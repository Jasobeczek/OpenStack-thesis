import json
from keystoneclient.v3.projects import ProjectManager as KSProjectManager
from keystoneclient.v3 import client as KSClient
from keystoneauth1.identity import v3 as KSIdentity
from keystoneauth1 import loading as KSloading
from keystoneauth1 import session as KSSession


class OSKeystone:
    client = None
    projectManager = None
    session = None

    def __init__(self, **kwargs):
        self.session = kwargs.get("session")
        self.client = KSClient.Client(session=self.session)
        self.projectManager = KSProjectManager(self.client)


class OSProject(OSKeystone):
    id = None
    name = None
    domain = None

    def __init__(self, **kwargs):
        """Init class
        Arguments:
            **kwargs -- id, name, domain, session
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.domain = kwargs.get("domain")
        self.session = kwargs.get("session")
        if self.session is not None:
            self.client = KSClient.Client(session=self.session)
            self.projectManager = KSProjectManager(self.client)

    def create(self, name, domain="default"):
        """Create new project
        This create new tenat and it is connected to current
        authorized user
        Arguments:
            name -- name of project
        Keyword arguments:
            domain -- slected domain (default: {"default"})
        Raises a {Exception}
        Return Poject classs
        """
        if self.find(name=name) is None:
            return self.client.projects.create(name, domain)
        else:
            raise Exception("Project " + name + " already exists!")

    def list(self):
        """Return list of projects"""
        return self.client.projects.list()

    def delete(self, project_id):
        """Delete selected project id"""
        return self.client.projects.delete(project_id)

    def get(self, project_id):
        """Get object of project by id"""
        return self.client.projects.get(project_id)

    def find(self, name):
        """Get object of project search by name"""
        projects = self.list()
        for project in projects:
            if project.name == name:
                return project
        return None


class OSUser(OSKeystone):
    username = None
    userDomain = None
    password = None

    def __init__(self, **kwargs):
        self.session = kwargs.get("session")
        self.client = KSClient.Client(session=self.session)
        self.projectManager = KSProjectManager(self.client)
        self.username = kwargs.get("username")
        self.userDomain = kwargs.get("userDomain")
        self.password = kwargs.get("password")

    def list(self):
        """List all users
        Returns:
            Array of user object
            Array
        """
        return self.client.users.list()

    def create(self, name, password, project_id, domain="default"):
        """Create new user
        Args:
            name: Name of user
            password: Password for this user
            project_id: Default project id can be null
            domain: What domain (default: {"default"})
        Returns:
            Created user in user class
            User
        Raises:
            Exception: Raise already exists!
        """
        users = self.find(name=name, project_id=project_id)
        if len(users) == 0:
            return self.client.users.create(name=name, password=password, default_project=project_id, domain=domain)
        else:
            raise Exception("User " + name + " already exists!")

    def delete(self, user_id):
        return self.client.users.delete(user_id)

    def get(self, user_id):
        return self.client.users.get(user_id)

    def find(self, **kwargs):
        """
        Find user by:
        - name
        - project_id
        - user_id
        Arguments:
            **kwargs -- name, project_id, user_id
        Returns:
            One users or array of users
            One item if item_id
            Array of users if project_id or name
            Mixed
        """
        name = kwargs.get("name")
        project_id = kwargs.get("project_id")
        user_id = kwargs.get("user_id")
        users = self.list()
        if user_id is not None:
            for i in range(0, len(users)):
                if users[i].id == user_id:
                    return users[i]

        if name is not None:
            if project_id is not None:
                returnArray = []
                for i in range(0, len(users)):
                    if users[i].name == name and hasattr(users[i], "default_project_id") and users[i].default_project_id == project_id:
                        returnArray.append(users[i])
                return returnArray
            else:
                returnArray = []
                for i in range(0, len(users)):
                    if users[i].name == name:
                        returnArray.append(users[i])
                return returnArray
        else:
            if project_id is not None:
                returnArray = []
                for i in range(0, len(users)):
                    if hasattr(users[i], "default_project_id") and users[i].default_project_id == project_id:
                        returnArray.append(users[i])
                return returnArray
            else:
                return None


class OSRole(OSKeystone):

    def list(self):
        return self.client.roles.list()

    def find(self, **kwargs):
        """
        Find user by:
        - name
        - role_id
        Arguments:
            **kwargs -- name, role_id
        Returns:
            One users or array of users
            One item if item_id
            Array of users if role_id or name
            Mixed
        """
        name = kwargs.get("name")
        role_id = kwargs.get("role_id")
        roles = self.list()
        if name is not None:
            if role_id is not None:
                returnArray = []
                for i in range(0, len(roles)):
                    if hasattr(roles[i], "name") and roles[i].name == name and hasattr(roles[i], "id") and roles[i].id == role_id:
                        returnArray.append(roles[i])
                return returnArray
            else:
                returnArray = []
                for i in range(0, len(roles)):
                    if hasattr(roles[i], "name") and roles[i].name == name:
                        returnArray.append(roles[i])
                return returnArray
        else:
            if role_id is not None:
                returnArray = []
                for i in range(0, len(roles)):
                    if hasattr(roles[i], "id") and roles[i].id == role_id:
                        returnArray.append(roles[i])
                return returnArray
            else:
                return None

    def grantUser(self, user_id, project_id, role_id):
        return self.client.roles.grant(role_id, user=user_id, project=project_id)

    def getUserRole(self, user_id):
        """Get name of roles connected with users
        Args:
            user_id: ID of user
        Returns:
            One or many names of roles
            Array
        """
        userRoles = self.client.role_assignments.list(user=user_id)
        if userRoles is not None:
            returnArray = []
            for i in range(0, len(userRoles)):
                if hasattr(userRoles[i], "role") and userRoles[i].role is not None:
                    role = userRoles[i].role
                    roles = self.find(role_id=role["id"])
                    if roles is not None:
                        returnArray.append(roles[0].name)
                else:
                    continue
            # Delete duplicates
            return list(set(returnArray))
        else:
            return None


class OSAuth:
    auth_url = None
    project_domain_name = None
    project_name = None
    project_id = None
    user_domain = None
    username = None
    password = None
    glance_endpoint = None

    def __init__(self, **kwargs):
        filename = kwargs.get("filename")
        if filename is None:
            self.auth_url = kwargs.get("auth_url")
            self.project_name = kwargs.get("project_name")
            self.project_domain_name = kwargs.get("project_domain_name")
            self.user_domain = kwargs.get("user_domain")
            self.username = kwargs.get("username")
            self.project_id = kwargs.get("project_id")
            self.password = kwargs.get("password")
            self.glance_endpoint = kwargs.get("glance_endpoint")
        else:
            self.getCredFromFile(filename)

    def __eq__(self, other):
        if self.auth_url == other.auth_url and self.project_name == other.project_name and self.project_domain_name == other.project_domain_name and self.user_domain == other.user_domain and self.username == other.username and self.password == other.password and self.project_id == other.project_id and self.glance_endpoint == other.glance_endpoint:
            return True
        else:
            return False

    def createKeyStoneSession(self):
        auth = KSIdentity.Password(
            user_domain_name=self.user_domain,
            username=self.username,
            password=self.password,
            project_domain_name=self.project_domain_name,
            project_name=self.project_name,
            project_id=self.project_id,
            auth_url=self.auth_url)
        return KSSession.Session(auth=auth)

    def createNovaSession(self):
        loader = KSloading.get_plugin_loader("password")
        auth = loader.load_from_options(
            user_domain_name=self.user_domain,
            auth_url=self.auth_url,
            username=self.username,
            password=self.password,
            project_domain_name=self.project_domain_name,
            project_name=self.project_name,
            project_id=self.project_id)
        return KSSession.Session(auth=auth)

    def getKeystoneCreds(self):
        d = {}
        d["username"] = self.username
        d["password"] = self.password
        d["auth_url"] = self.auth_url
        d["tenant_name"] = self.project_name
        return d

    def getCredFromFile(self, file_name):
        with open(file_name) as data_file:
            data = json.load(data_file)
            try:
                if "user_domain" in data:
                    self.user_domain = data["user_domain"]
                if "username" in data:
                    self.username = data["username"]
                if "password" in data:
                    self.password = data["password"]
                if "auth_url" in data:
                    self.auth_url = data["auth_url"]
                if "project_name" in data:
                    self.project_name = data["project_name"]
                if "project_domain_name" in data:
                    self.project_domain_name = data["project_domain_name"]
                if "project_id" in data:
                    self.project_id = data["project_id"]
                if "glance_endpoint" in data:
                    self.glance_endpoint = data["glance_endpoint"]
            except IndexError:
                print("JSON cred invalid!")

    def getProjectName(self):
        return self.project_name

    def getProjectID(self):
        return self.project_id