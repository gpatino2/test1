function evaluateTemplate() {
	var installTemplate = templateResolver.getTemplate('installApacheUbuntuTemplate', templateAttributes);
	return installTemplate;
}
evaluateTemplate();