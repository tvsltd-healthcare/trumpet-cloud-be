import os
import requests

from typing import List, Union, Optional

from dotenv import load_dotenv


load_dotenv()


AVAILABLE_DOS = os.getenv("DO_ENDPOINTS").split(",")


class BaseLogicInjector:
    def __init__(self):
        pass
    def inject_business_logic(self, entity_id: dict, entity: dict):
        # ToDo: generalize this for all the custom logics
        # Decode the dict from the entity
        entity= dict(entity)
        participants = entity.get('participants', '').split(",")

        # First call the Setup method in Trumpet Cloud's FL Core Agg
        fl_injector_obj = FLSetupInjector()

        agg_response = fl_injector_obj.call_setup_on_agg_fl_core(fl_agg_core_url=os.getenv('TC_FL_CORE_BASE_URL'),
                                                  name=str(entity_id.get('study_id', "")),
                                                  coordinator=os.getenv('COORDINATOR'),
                                                  model=entity.get('model', "NN_FHIR"),
                                                  pet=entity.get('pet', "None"),
                                                  rounds=entity.get('rounds', "3"),
                                                  webhook_url=os.getenv('LISTENER_WEBHOOK_URL'),
                                                  participants=participants)

        for do_endpoint in AVAILABLE_DOS:
            do_response = fl_injector_obj.call_setup_on_participants_do_fl_core(
                do_url=do_endpoint,
                name=str(entity_id.get('study_id', "")),
                coordinator=os.getenv('COORDINATOR'),
                model=entity.get('model', "NN_FHIR"),
                pet=entity.get('pet', "None"),
                rounds=entity.get('rounds', "3"),
                webhook_url=os.getenv('LISTENER_WEBHOOK_URL'),
                participants=participants,
                purpose=entity.get('purpose', ""),
                description=entity.get('description', "N/A"),
            )

            do_upload_data_response = fl_injector_obj.call_participants_do_fl_core_query(do_url=do_endpoint)

class FLSetupInjector:
    setup_uri = "/setup"
    do_load_data_uri = "/fl-core/load-data/"
    do_setup_uri = "/fl-core/setup/"

    def call_setup_on_agg_fl_core(self, fl_agg_core_url: str, name: str, coordinator: str, model: str, pet: str,
                                 rounds: str,
                                 webhook_url: str, participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {
            "name": name,
            "coordinator": coordinator,
            "model": model,
            "pet": pet,
            "rounds": rounds,
            "webhook_url": webhook_url,
            "participants": participants,
        }

        response = requests.post(url=fl_agg_core_url + self.setup_uri, json=_request_body)
        if response.status_code != 200:
            return False
        return True, response.json()

    def call_setup_on_participants_do_fl_core(self, do_url: str, name: str, coordinator: str, model: str, pet: str,
                                 rounds: str, description:str, purpose:str,
                                 webhook_url: str, participants: List[str]) -> Union[bool, tuple[bool, dict]]:
        _request_body = {
            "name": name,
            "coordinator": coordinator,
            "description": description,
            "purpose": purpose,
            "status": "active",
            "model": model,
            "pet": pet,
            "rounds": rounds,
            "webhook_url": webhook_url,
            "participants": participants,
        }

        response = requests.post(url=do_url + self.do_setup_uri, json=_request_body)
        if response.status_code != 200:
            return False
        return True, response.json()

    def call_participants_do_fl_core_query(self, do_url: str, query: Optional[str] = None):
        _request_body = None

        response = requests.post(url=do_url + self.do_load_data_uri, json=_request_body)
        if response.status_code != 200:
            return False
        return True, response.json()
