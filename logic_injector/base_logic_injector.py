import os
import requests

from typing import List, Union, Optional

from dotenv import load_dotenv

load_dotenv()

FL_COMMUNICATION_PORT = os.getenv("FL_COMMUNICATION_PORT", 8081)


class BaseLogicInjector:
    def __init__(self):
        pass

    def inject_business_logic(self, study_agreement: dict, do_org_agreements: list):
        """
        Args:
            study_agreement:
            do_org_agreements:
        Returns:
            None
        """

        do_org_agreements = sorted(do_org_agreements, key=lambda do_org_agreement: do_org_agreement["organization"]["id"])

        agreement_id = study_agreement.get('id')
        study_id = study_agreement.get('study_id')
        name = str(study_id)

        purpose = study_agreement.get('purpose', "")
        description = study_agreement.get('description', "N/A")

        coordinator = os.getenv('COORDINATOR')
        model = study_agreement.get('model', "NN_HNC")

        pet = study_agreement.get('pet')
        pet_config = study_agreement.get("pet_config")

        samples = study_agreement.get('samples', 80)
        rounds = study_agreement.get('rounds', "3")


        participants = [prepare_fl_core_communication_url(do_org_agreement) for do_org_agreement in do_org_agreements]
        webhook_url = os.getenv('LISTENER_WEBHOOK_URL')

        fl_injector_obj = FLSetupInjector()

        agg_response = fl_injector_obj.call_setup_on_agg_fl_core(fl_agg_core_url=os.getenv('TC_FL_CORE_BASE_URL'),
                                                                 agreement_id=agreement_id,
                                                                 name=name,
                                                                 coordinator=coordinator,
                                                                 model=model,
                                                                 pet=pet,
                                                                 pet_config=pet_config,
                                                                 rounds=rounds,
                                                                 webhook_url=webhook_url,
                                                                 participants=participants)

        for do_org_agreement in do_org_agreements:
            do_url = do_org_agreement['organization']['host']
            dataset_uid = do_org_agreement['dataset']['don_uid']
            do_response = fl_injector_obj.call_setup_on_participants_do_fl_core(do_url=do_url,
                                                                                agreement_id=agreement_id,
                                                                                name=name,
                                                                                coordinator=coordinator,
                                                                                model=model,
                                                                                pet=pet,
                                                                                pet_config=pet_config,
                                                                                rounds=rounds,
                                                                                webhook_url=webhook_url,
                                                                                participants=participants,
                                                                                purpose=purpose,
                                                                                description=description)

            do_upload_data_response = fl_injector_obj.call_participants_do_fl_core_query(do_url=do_url,
                                                                                         model=model,
                                                                                         dataset_uid=dataset_uid,
                                                                                         samples=samples)

class FLSetupInjector:
    setup_uri = "/setup"
    do_load_data_uri = "/fl-core/load-data/"
    do_setup_uri = "/fl-core/setup/"

    def call_setup_on_agg_fl_core(self, fl_agg_core_url: str, agreement_id: int, name: str, coordinator: str,
                                  model: str, pet: str, pet_config: dict, rounds: str, webhook_url: str,
                                  participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {"name": name, "study_id": str(agreement_id), "coordinator": coordinator, "model": model,
                         "pet": pet, "pet_config": pet_config, "rounds": rounds, "webhook_url": webhook_url,
                         "participants": participants, }

        print('call_setup_on_agg_fl_core request =====', _request_body)

        response = requests.post(url=fl_agg_core_url + self.setup_uri, json=_request_body, timeout=60)

        print('call_setup_on_agg_fl_core response =======', response)

        if response.status_code != 200:
            return False
        return True, response.json()

    def call_setup_on_participants_do_fl_core(self, do_url: str, agreement_id: int, name: str, coordinator: str,
                                              model: str, pet: str, pet_config: dict, rounds: str, description: str,
                                              purpose: str, webhook_url: str, participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {"name": name, "agreement_id": agreement_id, "coordinator": coordinator, "model": model,
                         "pet": pet, "pet_config": pet_config, "rounds": rounds, "webhook_url": webhook_url,
                         "participants": participants, }

        print('call_setup_on_participants_do_fl_core request =====', _request_body)

        response = requests.post(url=do_url + self.do_setup_uri, json=_request_body, timeout=60)

        print('call_setup_on_participants_do_fl_core response =====', response)

        if response.status_code != 200 or response.status_code != 201:
            return False
        return True, response.json()

    def call_participants_do_fl_core_query(self, do_url: str, model: str, dataset_uid: str, samples: Optional[int] = 80,
                                           query: Optional[str] = None):
        _request_body = {"model": model, "samples": samples, "dataset_uid": dataset_uid}

        print('call_participants_do_fl_core_query request =====', _request_body)

        response = requests.post(url=do_url + self.do_load_data_uri, json=_request_body, timeout=60)

        print('call_participants_do_fl_core_query request =====', response)

        if response.status_code != 200:
            return False
        return True, response.json()


def prepare_fl_core_communication_url(do_org_agreement):
    host = do_org_agreement['organization']['host']
    return f"{host.removeprefix('http://').removeprefix('https://').split(':')[0]}:{FL_COMMUNICATION_PORT}"
