import pytest

from att import app
from datetime import datetime, timedelta
from src.models.base import db

TEST_DATABASE_PATH = "sqlite:///example.sqlite"


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.fixture(autouse=True)
def database():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../tests/example.sqlite"
    db.init_app(app)
    db.drop_all()
    db.create_all()
    return database


@pytest.fixture
def current_billing_cycle():
    from src.models.cycles import BillingCycle
    billing_cycle = BillingCycle(
        start_date=datetime.today() - timedelta(days=30),
        end_date=datetime.today() + timedelta(days=30)
    )

    db.session.add(billing_cycle)
    db.session.commit()
    yield billing_cycle


@pytest.fixture
def plan():
    from src.models.service_codes import Plan
    plan = Plan(id=1, mb_available=1000)
    db.session.add(plan)
    db.session.commit()
    yield plan


@pytest.fixture
def subscription(plan):
    from src.models.subscriptions import (Subscription, SubscriptionStatus)
    subscription = Subscription(plan=plan, plan_id=plan.id, status=SubscriptionStatus.active)

    db.session.add(subscription)
    db.session.commit()
    yield subscription


@pytest.fixture
def data_usages(subscription):
    from src.models.usages import DataUsage

    data_usages_list = [
        DataUsage(mb_used=100, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=1),
                  to_date=datetime.today() + timedelta(days=4)),
        DataUsage(mb_used=200, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=5),
                  to_date=datetime.today() + timedelta(days=15)),
        DataUsage(mb_used=300, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=10),
                  to_date=datetime.today() + timedelta(days=4)),
        DataUsage(mb_used=10000, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=100),
                  to_date=datetime.today() - timedelta(days=70))
    ]

    db.session.add_all(data_usages_list)
    db.session.commit()
    return data_usages_list


@pytest.fixture
def data_usages_over_allocated(subscription):
    from src.models.usages import DataUsage

    data_usages_list = [
        DataUsage(mb_used=1000, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=1),
                  to_date=datetime.today() + timedelta(days=4)),
        DataUsage(mb_used=2000, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=5),
                  to_date=datetime.today() + timedelta(days=15)),
        DataUsage(mb_used=3000, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=10),
                  to_date=datetime.today() + timedelta(days=4)),
        DataUsage(mb_used=10000, subscription=subscription, subscription_id=subscription.id,
                  from_date=datetime.today() - timedelta(days=100),
                  to_date=datetime.today() - timedelta(days=70))
    ]

    db.session.add_all(data_usages_list)
    db.session.commit()
    return data_usages_list
