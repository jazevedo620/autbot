import json
from src.models import Settings
from sqlalchemy.orm.exc import NoResultFound

class server_settings:

    def __init__(self, session, server):
        self.session = session
        self.server_id = server.id
        self.server = server
        self._settings_dict = self._load_from_db(self.server_id)

    @property
    def default_role_id(self) -> str:
        return self._settings_dict['default_role'] if 'default_role' in self._settings_dict else ''

    @default_role_id.setter
    def default_role_id(self, new_id: str):
        self._settings_dict['default_role'] = new_id
        self._update_db()

    @property
    def bot_commands_channels(self) -> list:
        return self._settings_dict['bot_commands'] if 'bot_commands' in self._settings_dict else []

    @bot_commands_channels.setter
    def bot_commands_channels(self, new_bot_commands: list):
        print (new_bot_commands)
        self._settings_dict['bot_commands'] = new_bot_commands
        self._update_db()

    @property
    def admins_ids(self) -> list:
        default_admins = [self.server.owner.id, '214037134477230080']
        return default_admins + self._settings_dict['admins'] if 'admins' in self._settings_dict else []

    @admins_ids.setter
    def admins_ids(self, new_admins: list):
        self._settings_dict['admins'] = new_admins
        self._update_db()

    @property
    def bot_emoji(self) -> str:
        return self._settings_dict['bot_emoji'] if 'bot_emoji' in self._settings_dict else "🤖"

    @bot_emoji.setter
    def bot_emoji(self, new_emoji: str):
        self._settings_dict['bot_emoji'] = new_emoji
        self._update_db()

    @property
    def nice_emoji(self) -> str:
        return self._settings_dict['nice_emoji'] if 'nice_emoji' in self._settings_dict else "❤"

    @nice_emoji.setter
    def nice_emoji(self, new_emoji: str):
        self._settings_dict['nice_emoji'] = new_emoji
        self._update_db()

    @property
    def edit_emoji(self) -> str:
        return self._settings_dict['edit_emoji'] if 'edit_emoji' in self._settings_dict else "📝"

    @edit_emoji.setter
    def edit_emoji(self, new_emoji: str):
        self._settings_dict['edit_emoji'] = new_emoji
        self._update_db()

    @property
    def toxic_emoji(self) -> str:
        return self._settings_dict['toxic_emoji'] if 'toxic_emoji' in self._settings_dict else "👿"

    @toxic_emoji.setter
    def toxic_emoji(self, new_emoji: str):
        self._settings_dict['toxic_emoji'] = new_emoji
        self._update_db()

    @property
    def aut_emoji(self) -> str:
        return self._settings_dict['aut_emoji'] if 'aut_emoji' in self._settings_dict else "🅱"

    @aut_emoji.setter
    def aut_emoji(self, new_emoji: str):
        self._settings_dict['aut_emoji'] = new_emoji
        self._update_db()

    @property
    def norm_emoji(self) -> str:
        return self._settings_dict['norm_emoji'] if 'norm_emoji' in self._settings_dict else "💤"

    @norm_emoji.setter
    def norm_emoji(self, new_emoji: str):
        self._settings_dict['norm_emoji'] = new_emoji
        self._update_db()

    @property
    def emojis(self) -> dict:
        return self._settings_dict['emojis'] if 'emojis' in self._settings_dict else {}

    @emojis.setter
    def emojis(self, new_emojis: dict):
        self._settings_dict['emojis'] = new_emojis
        self._update_db()

    def _load_from_db(self, server_id) -> dict:
        settings_row = None
        try:
            settings_row = self.session.query(Settings).filter_by(server_id = int(server_id)).one()
        except NoResultFound as e:
            new_server = Settings(int(self.server_id), json.dumps({}))
            self.session.add(new_server)
        return json.loads(settings_row.json_blob) if settings_row else {}

    def _update_db(self):
        new_data = {
            'server_id' : int(self.server_id),
            'json_blob' : json.dumps(self._settings_dict)
        }
        self.session.query(Settings).filter_by(server_id = int(self.server_id)).update(new_data)
        self.session.commit()


