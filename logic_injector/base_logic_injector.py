import os
import requests

from typing import List, Union, Optional

from dotenv import load_dotenv

load_dotenv()

FL_COMMUNICATION_PORT = os.getenv("FL_COMMUNICATION_PORT", 8081)


class BaseLogicInjector:
    def __init__(self):
        pass

    def inject_business_logic(self, entity_id: dict, entity: dict, agreement_id: int, host_list: list[str]):
        # ToDo: generalize this for all the custom logics
        # Decode the dict from the entity
        entity = dict(entity)
        print('host_list', host_list)
        participants = list(map(lambda host: f"{host.removeprefix('http://').removeprefix('https://').split(':')[0]}:{FL_COMMUNICATION_PORT}",
                                host_list)) if host_list else []

        # First call the Setup method in Trumpet Cloud's FL Core Agg
        fl_injector_obj = FLSetupInjector()

        agg_response = fl_injector_obj.call_setup_on_agg_fl_core(fl_agg_core_url=os.getenv('TC_FL_CORE_BASE_URL'),
                                                                 agreement_id=agreement_id,
                                                                 name=str(entity_id.get('study_id', "")),
                                                                 coordinator=os.getenv('COORDINATOR'),
                                                                 model=entity.get('model', "NN_HNC"),
                                                                 pet=entity.get('pet'),
                                                                 pet_config=entity.get("pet_config"),
                                                                 rounds=entity.get('rounds', "3"),
                                                                 webhook_url=os.getenv('LISTENER_WEBHOOK_URL'),
                                                                 participants=participants)

        for do_endpoint in host_list:
            do_response = fl_injector_obj.call_setup_on_participants_do_fl_core(do_url=do_endpoint,
                                                                                agreement_id=agreement_id,
                                                                                name=str(entity_id.get('study_id', "")),
                                                                                coordinator=os.getenv('COORDINATOR'),
                                                                                model=entity.get('model', "NN_HNC"),
                                                                                pet=entity.get('pet'),
                                                                                pet_config=entity.get("pet_config"),
                                                                                rounds=entity.get('rounds', "3"),
                                                                                webhook_url=os.getenv('LISTENER_WEBHOOK_URL'),
                                                                                participants=participants,
                                                                                purpose=entity.get('purpose', ""),
                                                                                description=entity.get('description', "N/A"), )

            do_upload_data_response = fl_injector_obj.call_participants_do_fl_core_query(do_url=do_endpoint,
                                                                                         model=entity.get('model', "NN_HNC"),
                                                                                         samples=entity.get('samples', 80))


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

        response = requests.post(url=fl_agg_core_url + self.setup_uri, json=_request_body)

        print('call_setup_on_agg_fl_core response =======', response)

        if response.status_code != 200:
            return False
        return True, response.json()

    def call_setup_on_participants_do_fl_core(self, do_url: str, agreement_id: int, name: str, coordinator: str,
                                              model: str, pet: str, pet_config: dict, rounds: str, description: str,
                                              purpose: str, webhook_url: str, participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {"name": name, "agreement_id": str(agreement_id), "coordinator": coordinator, "model": model,
                         "pet": pet, "pet_config": pet_config, "rounds": rounds, "webhook_url": webhook_url,
                         "participants": participants, }

        print('call_setup_on_participants_do_fl_core request =====', _request_body)

        response = requests.post(url=do_url + self.do_setup_uri, json=_request_body)

        print('call_setup_on_participants_do_fl_core response =====', response)

        if response.status_code != 200 or response.status_code != 201:
            return False
        return True, response.json()

    def call_participants_do_fl_core_query(self, do_url: str, model: str, samples: Optional[int] = 80,
                                           query: Optional[str] = None):
        _request_body = {"model": model, "dataset_id": "HNC"}
        if samples:
            _request_body["samples"] = samples

        response = requests.post(url=do_url + self.do_load_data_uri, json=_request_body)
        if response.status_code != 200:
            return False
        return True, response.json()
