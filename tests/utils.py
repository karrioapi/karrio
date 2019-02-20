from gds_helpers import to_xml


""" strip tabs, new line characters and spaces from text  """


def strip(text: str) -> str:
    return text.replace("\t", "").replace("\n", "").replace(" ", "")


""" dump XML from string and retrieve (first) node from it """


def get_node_from_xml(xml_str: str, node_name: str) -> "XMLElement":
    return to_xml(xml_str).xpath(".//*[local-name() = $name]", name=node_name)[0]
