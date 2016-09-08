def test_only_scheduler_can_cancel_prior_to_target_block(deploy_client,
                                                         deployed_contracts,
                                                         deploy_future_block_call,
                                                         CallLib):
    client_contract = deployed_contracts.TestCallExecution

    target_block = deploy_client.get_block_number() + 300
    call = deploy_future_block_call(
        client_contract.setBool,
        target_block=target_block,
    )

    assert call.isCancelled() is False

    cancel_txn_hash = call.cancel(_from=encode_hex(accounts[1]))
    cancel_txn_receipt = deploy_client.wait_for_transaction(cancel_txn_hash)
    assert len(CallLib.Cancelled.get_transaction_logs(cancel_txn_hash)) == 0
