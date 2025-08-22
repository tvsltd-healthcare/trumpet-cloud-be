import os
import requests

from typing import List, Union, Optional

from dotenv import load_dotenv
from domain_layer.auth_manager import AuthManager

load_dotenv()

FL_COMMUNICATION_PORT = os.getenv("FL_COMMUNICATION_PORT", 8081)
FL_TOKEN_EXPIRY = os.getenv("FL_TOKEN_EXPIRY", 3600)


class BaseLogicInjector:
    def __init__(self):
        pass

    def generate_token(self, payload: dict):
        auth_getter_adapter = AuthManager.get()
        payload["expiry"] = int(FL_TOKEN_EXPIRY)
        token_dict = auth_getter_adapter.generate_token(payload)
        return token_dict['token']

    def inject_business_logic(self, study_agreement: dict, do_org_agreements: list):
        """
        Args:
            study_agreement:
            do_org_agreements:
        Returns:
            None
        """

        agreement_id = study_agreement.get('id')
        study_id = study_agreement.get('study_id')
        name = str(study_id)

        purpose = study_agreement.get('purpose', "")
        description = study_agreement.get('description', "N/A")

        coordinator = os.getenv('COORDINATOR')
        model = study_agreement.get('model')

        label = study_agreement.get('label')

        pet = study_agreement.get('pet')
        pet_config = study_agreement.get("pet_config")

        samples = study_agreement.get('samples', 80)
        rounds = study_agreement.get('rounds', "3")


        participants = [prepare_fl_core_communication_url(do_org_agreement) for do_org_agreement in do_org_agreements]
        webhook_url = os.getenv('LISTENER_WEBHOOK_URL')

        fl_injector_obj = FLSetupInjector()

        fl_core_token = self.generate_token(payload={
            'type': 'agg_fl_core',
            'study_agreement_id': agreement_id,
        })

        agg_response = fl_injector_obj.call_setup_on_agg_fl_core(fl_agg_core_url=os.getenv('TC_FL_CORE_BASE_URL'),
                                                                 agreement_id=agreement_id,
                                                                 name=name,
                                                                 coordinator=coordinator,
                                                                 model=model,
                                                                 label=label,
                                                                 pet=pet,
                                                                 pet_config=pet_config,
                                                                 rounds=rounds,
                                                                 webhook_url=f"{webhook_url}/{fl_core_token}",
                                                                 participants=participants)

        for index, do_org_agreement in enumerate(do_org_agreements):
            do_url = do_org_agreement['organization']['host']
            dataset_uid = do_org_agreement['dataset']['don_uid']

            do_token = self.generate_token(payload={
                'type': 'do_fl_core',
                'study_agreement_id': agreement_id,
                'organization_id': do_org_agreement['organization']['id'],
                'dataset_id': do_org_agreement['dataset']['id']
            })

            do_response = fl_injector_obj.call_setup_on_participants_do_fl_core(do_url=do_url,
                                                                                agreement_id=agreement_id,
                                                                                name=name,
                                                                                coordinator=coordinator,
                                                                                model=model,
                                                                                label=label,
                                                                                pet=pet,
                                                                                pet_config=pet_config,
                                                                                rounds=rounds,
                                                                                webhook_url=f"{webhook_url}/{do_token}",
                                                                                participants=participants,
                                                                                purpose=purpose,
                                                                                description=description,
                                                                                node_id=f"{index+1}")

            do_upload_data_response = fl_injector_obj.call_participants_do_fl_core_query(do_url=do_url,
                                                                                         label=label,
                                                                                         dataset_uid=dataset_uid,
                                                                                         samples=samples)

class FLSetupInjector:
    setup_uri = "/setup"
    do_load_data_uri = "/fl-core/load-data/"
    do_setup_uri = "/fl-core/setup/"

    def call_setup_on_agg_fl_core(self, fl_agg_core_url: str, agreement_id: int, name: str, coordinator: str,
                                  model: str, label: str, pet: str, pet_config: dict, rounds: str, webhook_url: str,
                                  participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        request_body = {"name": name, "study_id": str(agreement_id), "coordinator": coordinator, "model": model, "label": label,
                         "pet": pet, "pet_config": pet_config, "rounds": rounds, "webhook_url": webhook_url,
                         "participants": participants, "node_id": "0"}

        print(f"CallingData FLCore aggregator {fl_agg_core_url + self.setup_uri} endpoint\nRequest Body:\n{request_body}")

        response = requests.post(url=fl_agg_core_url + self.setup_uri, json=request_body, timeout=60)

        print(f"Called FLCore aggregator Post {fl_agg_core_url+self.setup_uri} endpoint\nResponse:\n{response}")

        if response.status_code != 200:
            return False
        return True, response.json()

    def call_setup_on_participants_do_fl_core(self, do_url: str, agreement_id: int, name: str, coordinator: str,
                                              model: str, label: str, pet: str, pet_config: dict, rounds: str, description: str,
                                              purpose: str, webhook_url: str, participants: List[str], node_id: str) -> Union[bool, tuple[bool, dict]]:
        request_body = {"name": name, "agreement_id": agreement_id, "coordinator": coordinator, "model": model, "label": label,
                         "pet": pet, "pet_config": pet_config, "rounds": rounds, "webhook_url": webhook_url,
                         "participants": participants, "node_id": node_id}

        print(f"CallingData Owner Node Post {do_url + self.do_setup_uri} endpoint\nRequest Body:\n{request_body}")

        response = requests.post(url=do_url + self.do_setup_uri, json=request_body, timeout=60)

        print(f"Called Data Owner Node Post {do_url+self.do_setup_uri} endpoint\nResponse:\n{response}")

        if response.status_code != 200 or response.status_code != 201:
            return False
        return True, response.json()

    def call_participants_do_fl_core_query(self, do_url: str, label: str, dataset_uid: str, samples: Optional[int] = 80,
                                           query: Optional[str] = None):
        request_body = {"label": label, "samples": samples, "dataset_uid": dataset_uid}

        print(f"CallingData Owner Node Post {do_url+self.do_load_data_uri} endpoint\nRequest Body:\n{request_body}")

        response = requests.post(url=do_url + self.do_load_data_uri, json=request_body, timeout=60)

        print(f"Called Data Owner Node Post {do_url+self.do_load_data_uri} endpoint\nResponse:\n{response}")

        if response.status_code != 200:
            return False
        return True, response.json()


def prepare_fl_core_communication_url(do_org_agreement):
    host = do_org_agreement['organization']['host']
    return f"{host.removeprefix('http://').removeprefix('https://').split(':')[0]}:{FL_COMMUNICATION_PORT}"
