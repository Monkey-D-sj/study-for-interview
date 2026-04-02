def parse_xml(xml_str: str, tag: str) -> str | None:
	start = xml_str.find(f"<{tag}>")
	if start == -1:
		return None
	end = xml_str.find(f"</{tag}>", start)
	return xml_str[start:end]