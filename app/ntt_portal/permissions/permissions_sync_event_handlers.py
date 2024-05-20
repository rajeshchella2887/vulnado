import logging

from ntt_portal_library.contracts.enums import MicroServiceEnum
from ntt_portal_library.message_queue.constants import ntt_permissions_mq
from ntt_portal_library.message_queue.utils.helpers import ProducerHelper

logger = logging.getLogger(__name__)


def pre_perm_registry_sync_func(sender, **kwargs):
    logger.debug(f"pre_perm_registry_sync_func: {sender}, {kwargs}")


def post_perm_registry_sync_func(sender, **kwargs):
    logger.debug(f"post_perm_registry_sync_func: {sender}, {kwargs}")

    # NOTE: we don't need to send the signal to the message queue
    # NOTE: signal is a class which is not json serializable
    kwargs.pop("signal")

    # NOTE: we need to add a sent_from field to the kwargs so that we can register it in global permission registry
    # NOTE: adding attr like this to avoid using GlobalPermissionRegistryData
    kwargs["sent_from"] = MicroServiceEnum.NTT_PORTAL.value

    (
        ProducerHelper()
        .use_default_connection()
        .define_exchange(ntt_permissions_mq.exchange_name, ntt_permissions_mq.exchange_type)
        .publish_message(
            kwargs,
            backup=True,
            sent_from=MicroServiceEnum.NTT_PORTAL.value,
            routing_key=ntt_permissions_mq.routing_key,
        )
    )
