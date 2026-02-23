import logging


class BaseTest:
    logger = logging.getLogger(__name__)

    @staticmethod
    def get_marker(request, marker_name):
        marker = request.node.get_closest_marker(marker_name)
        return marker.args[0] if marker else None

    def log_test_metadata(self, request):
        jira_id = self.get_marker(request, "jira")
        testrail_id = self.get_marker(request, "testrail")
        self.logger.info(f"Jira ID: {jira_id}, TestRail ID: {testrail_id}")
