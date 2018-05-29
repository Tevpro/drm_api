from zeep import Client as zeepClient
from zeep.wsse.username import UsernameToken
from zeep import xsd
from lxml import etree
from .Access import Access
from .Api import Api
from zeep.xsd.schema import Schema

class Client:

    def __init__(self, web_service: Api = None, drm_adapter: Api = None):
        if web_service:
            if type(web_service) == str:
                web_service = Api(web_service)
            self.api = web_service
        if drm_adapter:
            if type(drm_adapter) == str:
                drm_adapter = Api(drm_adapter)
            self.adapter = drm_adapter
        Access = self.enum(Standard='Standard', System='System', User='User')

    @property
    def get_header(self):
        header_def = xsd.Element(
            '{http://drm.webservices.epm.oracle}AppParameters',
            xsd.ComplexType([
                xsd.Element("{http://drm.webservices.epm.oracle}serverUrl",
                            xsd.String()
                            ),
                xsd.Element("{http://drm.webservices.epm.oracle}sessionParams",
                            xsd.String()
                            )
            ])
        )
        return header_def(serverUrl=self.adapter.end_point,
                          sessionParams="ProductVersion=11.1.2,CultureName=en-US,TimeZoneOffset=-360")

    @property
    def get_client(self):
        ws: Api = self.api
        client = zeepClient(ws.end_point + '?wsdl', wsse=UsernameToken(ws.username, ws.password))
        client.set_default_soapheaders([self.get_header])
        client.raw_response = True
        #with client.options(raw_response=False):
        return client

    @property
    def access(self):
        return self.enum(Standard='Standard', System='System', User='User')

    @staticmethod
    def enum(**named_values):
        return type('Enum', (), named_values)

    def delete_property(self, name: str):
        return self.get_client.service.deletePropDef(propDefName=name)

    def delete_export(self, name: str, access: Access = Access.Standard):
        return self.get_client.service.deleteExport(exportName=name, access=access.value)

    def delete_query(self, name: str, access: Access = Access.Standard):
        return self.get_client.service.deleteQuery(queryName=name, objectAccess=access.value)

    def delete_book(self, name: str, access: Access = Access.Standard):
        return self.get_client.service.deleteBook(bookName=name, access=access.value)

    def delete_compare(self, name: str, access: Access = Access.Standard):
        return self.get_client.service.deleteCompare(compareName=name, access=access.value)

    def delete_domain(self, name: str):
        return self.get_client.service.deleteDomain(name=name)

    def delete_hier(self, name: str, version: str):
        return self.get_client.service.deleteHier(versionName=version, hierName=name)

    def delete_orphan_nodes(self, version: str, nodes: list, merge: list):
        return self.get_client.service.deleteOrphanNodes(versionName=version, nodeNames=nodes, mergeNodes=merge)

    def delete_blender(self, name: str, access: Access = Access.Standard):
        return self.get_client.service.deleteBlender(blenderName=name, access=access.value)

    def delete_import(self, name: str, access: Access = Access.Standard):
        return self.get_client.service.deleteImport(importName=name, access=access.value)

    def delete_node_type(self, name: str):
        return self.get_client.service.deleteNodeType(nodeTypeName=name)

    def delete_hier_group(self, name: str):
        return self.get_client.service.deleteHierGroup(groupName=name)

    def delete_validation(self, name: str):
        return self.get_client.service.deleteValidation(validationName=name)

    def delete_user(self, name: str):
        return self.get_client.service.deleteUser(userName=name)

    def delete_request(self, id: int):
        return self.get_client.service.deleteRequest(requestId=id)

    def delete_node(self, version: str, hierarchy: str, node: str, merge: str = "", destroy: bool = False):
        return self.get_client.service.deleteNode(versionName=version, hierName=hierarchy, nodeName=node,
                                                  mergeNodeName=merge, destroyNode=destroy)

    def delete_node_access_group(self, name: str):
        return self.get_client.service.deleteNodeAccessGroup(nodeAccessGroupName=name)

    def delete_nodes(self, version: str, hierarchy: str, nodes: list =[], merge: list = [],
                     destroy: bool = False):
        return self.get_client.service.deleteNodes(versionName=version, hierName=hierarchy, nodeNameList=nodes,
                                                   mergeNodeNameList=merge, destroyNodes=destroy)

    def delete_glyph(self, name: str):
        return self.get_client.service.deelteGlyph(glyphName=name)

    def get_node_types(self):
        resp = self.get_client.service.getNodeTypes()
        if resp.status_code == 500:
            return Error.from_response(resp)
        return resp

    def get_prop_def(self, name):
        return self.get_client.service.getPropDef(propDefName=name)

    def start_book(self, name: str, from_version: str, to_version: str=None, access: Access = Access.Standard):
        if not to_version:
            to_version = from_version
        response = self.get_client.service.startBookByName(bookName=name, access=access.value, fromVersionName=from_version,
                                                       toVersionName=to_version)
        return JobInfo.from_book(response, self)

    def job_status(self, id=None, name=None):
        return self.get_client.service.getJobStatus(jobInfo={'id': id })


class JobInfo:

    def __init__(self, id, name, machine=None, process_id=0, thread_id=0, session=None, status=None, percent=None,
                 message=None, client: Client=None):
        self.id = id
        self.name = name
        self.machine = machine
        self.process_id = process_id
        self.thread_id = thread_id
        self.session = session
        self.status = status
        self.percent = percent
        self.message = message
        self.client = client

    @staticmethod
    def from_book(content, client=None):
        root = etree.fromstring(content.text)
        name = root.find('.//{http://drm.webservices.epm.oracle}name', namespaces=root.nsmap)
        machine = root.find('.//{http://drm.webservices.epm.oracle}machineName', namespaces=root.nsmap)
        return JobInfo(
            id=root.find('.//{http://drm.webservices.epm.oracle}id', namespaces=root.nsmap).text,
            name=name.text if name is not None else None,
            machine=machine.text if machine is not None else None,
            process_id=root.find('.//{http://drm.webservices.epm.oracle}processId', namespaces=root.nsmap).text,
            thread_id=root.find('.//{http://drm.webservices.epm.oracle}threadId', namespaces=root.nsmap).text,
            session=root.find('.//{http://drm.webservices.epm.oracle}session', namespaces=root.nsmap).text,
            status=root.find('.//{http://drm.webservices.epm.oracle}status', namespaces=root.nsmap).text,
            percent=root.find('.//{http://drm.webservices.epm.oracle}percentComplete', namespaces=root.nsmap).text,
            message=root.find('.//{http://drm.webservices.epm.oracle}progressMessage', namespaces=root.nsmap).text,
            client=client)

    @property
    def is_complete(self):
        return self.status == "Done"

    def update(self):
        return self.from_book(self.client.job_status(self.id), self.client)