import os
import requests

from typing import List, Union, Optional

from dotenv import load_dotenv


load_dotenv()


FL_COMMUNICATION_PORT = os.getenv("FL_COMMUNICATION_PORT", 8081)

PET_CONFIG_MAP = {
        'None': {},
        'CDC_DP': {
            "eval_points": [0.001, 0.002, 0.003],
            "eps1": 0.5,
            "eps3": 10,
            "epochs": 1,
            "release_proportion": 0.3,
            "eps2": 0.5,
            "gamma": 1,
            "tau": 1e-10,
        },
        'ThHE': {
            "logn": 16,
            "plaintext_mod": 0,
            "log_q": [58, 56, 55, 55],
            "log_p": [56, 55],
            "scale": 16,
        }
    }


class BaseLogicInjector:
    def __init__(self):
        pass

    def inject_business_logic(self, entity_id: dict, entity: dict, agreement_id: int, host_list: list[str]):
        # ToDo: generalize this for all the custom logics
        # Decode the dict from the entity
        entity= dict(entity)
        participants = list(
            map(
                lambda host: f"{host.removeprefix('http://')}:{FL_COMMUNICATION_PORT}",
                host_list
            )
        ) if host_list else []

        # First call the Setup method in Trumpet Cloud's FL Core Agg
        fl_injector_obj = FLSetupInjector()

        agg_response = fl_injector_obj.call_setup_on_agg_fl_core(fl_agg_core_url=os.getenv('TC_FL_CORE_BASE_URL'),
                                                  agreement_id=agreement_id,
                                                  name=str(entity_id.get('study_id', "")),
                                                  coordinator=os.getenv('COORDINATOR'),
                                                  model=entity.get('model', "NN_HNC"),
                                                  pet=entity.get('pet', "None"),
                                                  rounds=entity.get('rounds', "3"),
                                                  webhook_url=os.getenv('LISTENER_WEBHOOK_URL'),
                                                  participants=participants)
        
        for do_endpoint in host_list:
            do_response = fl_injector_obj.call_setup_on_participants_do_fl_core(
                do_url=do_endpoint,
                agreement_id=agreement_id,
                name=str(entity_id.get('study_id', "")),
                coordinator=os.getenv('COORDINATOR'),
                model=entity.get('model', "NN_HNC"),
                pet=entity.get('pet', "None"),
                rounds=entity.get('rounds', "3"),
                webhook_url=os.getenv('LISTENER_WEBHOOK_URL'),
                participants=participants,
                purpose=entity.get('purpose', ""),
                description=entity.get('description', "N/A"),
            )

            do_upload_data_response = fl_injector_obj.call_participants_do_fl_core_query(
                do_url=do_endpoint, model=entity.get('model', "NN_HNC"), samples = entity.get('samples', 1000))

class FLSetupInjector:
    setup_uri = "/setup"
    do_load_data_uri = "/fl-core/load-data/"
    do_setup_uri = "/fl-core/setup/"

    def call_setup_on_agg_fl_core(self, fl_agg_core_url: str, agreement_id: int, name: str, coordinator: str, model: str, pet: str,
                                 rounds: str,
                                 webhook_url: str, participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {
            "name": name,
            "study_id": str(agreement_id),
            "coordinator": coordinator,
            "model": model,
            "pet": pet,
            "pet_config" : PET_CONFIG_MAP[pet],
            "rounds": rounds,
            "webhook_url": webhook_url,
            "participants":  participants,
        }

        response = requests.post(url=fl_agg_core_url + self.setup_uri, json=_request_body)

        if response.status_code != 200:
            return False
        return True, response.json()

    def call_setup_on_participants_do_fl_core(self, do_url: str, agreement_id: int, name: str, coordinator: str, model: str, pet: str,
                                 rounds: str, description:str, purpose:str,
                                 webhook_url: str, participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {
            "name": name,
            "agreement_id": str(agreement_id),
            "coordinator": coordinator,
            "model": model,
            "pet": pet,
            "pet_config" : PET_CONFIG_MAP[pet],
            "rounds": rounds,
            "webhook_url": webhook_url,
            "participants":  participants,
        }

        response = requests.post(url=do_url + self.do_setup_uri, json=_request_body)

        print('do response --------', response)

        if (response.status_code != 200 or response.status_code != 201):
            return False
        return True, response.json()

    def call_participants_do_fl_core_query(self, do_url: str, model: str, samples: Optional[int] = 1000, query: Optional[str] = None):
        _request_body = {
            "model": model,
        }
        if samples:
            _request_body["sample"] = samples

        response = requests.post(url=do_url + self.do_load_data_uri, json=_request_body)
        if response.status_code != 200:
            return False
        return True, response.json()
