"""Usage resource for handling any usage requests"""
from flask import jsonify
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from src.models.cycles import BillingCycle
from src.models.subscriptions import Subscription
from src.schemas.data_usage import DataUsagesAmongSchema, StatusDataUsagesAmong


class DataUsagesAmongError(NotFound):
    pass


class DataUsagesAmongAPI(Resource):
    """Resource/routes for DataUsage Among endpoints"""
    GB_MEMORY_RATE = 1000

    def _calculate_among_data_usage(self, data_usage):
        """Calculate among data usage in GB"""

        if not data_usage:
            return 0

        mb_used_list = [
            data_usage.mb_used
            for data_usage in data_usage
        ]
        return float(sum(mb_used_list)) / self.GB_MEMORY_RATE

    def _elaborate_status(self, gb_used, plan):
        """Prepare response status"""
        if plan.is_unlimited:
            return StatusDataUsagesAmong.succeed

        if plan.mb_available > gb_used * self.GB_MEMORY_RATE:
            return StatusDataUsagesAmong.succeed
        return StatusDataUsagesAmong.error

    def among_data_usage(self, data_usages, plan):
        """Return dictionary for DataUsageAmongSchema objtect"""

        if not data_usages:
            raise DataUsagesAmongError("Not found data usages to prepare among data usage for this subscription.")

        gb_used = self._calculate_among_data_usage(data_usages)
        status = self._elaborate_status(gb_used, plan)

        response = {
            'gb_used': gb_used,
            'status': status
        }
        return response

    def get(self, sid):
        """External facing DataUsage endpoint GET

        Gets an existing DataUsage objects for the current billing cycle and elaborate used memory.

        Args:
            sid (int): id of subscription object

        Returns:
            json: serialized DataUsagesAmong object

        """
        billing_cycle = BillingCycle.current_billing_cycle()
        subscription = Subscription.get_and_validate_subscription(sid)

        data_usages = list(filter(
            lambda data_usage: data_usage.validate_billing_cycle_date(billing_cycle),
            subscription.data_usages
        ))

        among_data_usage = self.among_data_usage(data_usages, subscription.plan)

        result = DataUsagesAmongSchema().dump(among_data_usage)
        return jsonify(result.data)
