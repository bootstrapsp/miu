import json
import os
import sys
from indy import pool as indy_pool


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR+'/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))


from ..identityLayer import identitylayer_pb2
from ..identityLayer import identitylayer_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_value(value, value_type=None):
    """
    This function return the value of the specified key else `None`

    For `strings`, the default value is the empty string.
    For `bytes`, the default value is empty bytes.
    For `bools`, the default value is false.
    For `numeric` types, the default value is zero.
    For `enums`, the default value is the first defined enum value, which must be 0.
    For message fields, the field is not set. Its exact value is language-dependent. See the generated code guide for details.
    The default value for `repeated` fields is empty (generally an empty list in the appropriate language).


    """
    # print('\n\n----------')
    # print(value, value_type, type(value))

    # string check
    if isinstance(value, str) and len(value) == 0:
        return None
    elif isinstance(value, str):
        return value

    # numeric check
    if isinstance(value, int) and value == 0:
        return None
    elif isinstance(value, int):
        return value



class PoolServiceServicer(identitylayer_pb2_grpc.PoolServiceServicer):
    """`pool` Services
    """

    async def CreatePoolLedgerConfig(self, request, context):
        """Create Pool Ledger Config
        """
        resp = None
        try:
            config_name = get_value(request.ConfigName)
            config = json.dumps({"genesis_txn": get_value(request.Config.GensisTxn)})

            resp = await indy_pool.create_pool_ledger_config(config_name, config)
            return identitylayer_pb2.CreatePoolLedgerConfigResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ CreatePoolLedgerConfig ------")
            logger.error(e)
            return identitylayer_pb2.CreatePoolLedgerConfigResponse(resp)


    async def OpenPoolLedger(self, request, context):
        """Open Pool Ledger
        """
        resp = None
        try:
            config_name = get_value(request.ConfigName)
            config = json.dumps({"timeout": get_value(request.Config.Timeout),
                "extended_timeout":get_value(request.Config.ExtendedTimeour),
                "preordered_nodes":get_value(request.Config.PreorderedNodes)})

            resp = await indy_pool.open_pool_ledger(config_name, config)
            return identitylayer_pb2.OpenPoolLedgerResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ OpenPoolLedger------")
            logger.error(e)
            return identitylayer_pb2.OpenPoolLedgerResponse(resp)

    async def RefreshPoolLedger(self, request, context):
        """Refresh Pool Ledger
        """
        resp = None
        try:
            handle = get_value(request.Handle)
            resp = await indy_pool.refresh_pool_ledger(handle)
            return identitylayer_pb2.RefreshPoolLedgerResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ RefreshPoolLedger------")
            logger.error(e)
            return identitylayer_pb2.RefreshPoolLedgerResponse(resp)

    async def ListPools(self, request, context):
        """List Pools
        """
        resp = None
        try:
            resp = await indy_pool.list_pools()
            return identitylayer_pb2.ListPoolsResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ ListPools------")
            logger.error(e)
            return identitylayer_pb2.ListPoolsResponse(resp)

    async def ClosePoolLedger(self, request, context):
        """Close Pool Ledger
        """
        resp = None
        try:
            handle = get_value(request.Handle)
            resp = await indy_pool.close_pool_ledger(handle)
            return identitylayer_pb2.ClosePoolLedgerResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ ClosePoolLedger------")
            logger.error(e)
            return identitylayer_pb2.ClosePoolLedgerResponse(resp)

    async def DeletePoolLedgerConfig(self, request, context):
        """Delete Pool Ledger Config
        """
        resp = None
        try:
            config_name = get_value(request.ConfigName)
            resp = await indy_pool.delete_pool_ledger_config(config_name)
            return identitylayer_pb2.DeletePoolLedgerConfigResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ DeletePoolLedgerConfig------")
            logger.error(e)
            return identitylayer_pb2.DeletePoolLedgerConfigResponse(resp)

    async def SetProtocolVersion(self, request, context):
        """Set Protocol Version
        """
        resp = None
        try:
            protocol_version = get_value(request.ProtocolVersion)
            resp = await indy_pool.set_protocol_version(protocol_version)
            return identitylayer_pb2.SetProtocolVersionResponse(resp)
        except Exception as e:
            logger.error("Exception Occurred @ SetProtocolVersion------")
            logger.error(e)
            return identitylayer_pb2.SetProtocolVersionResponse(resp)
