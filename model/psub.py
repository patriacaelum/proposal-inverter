# from .behavior import update_a
from .model.allocate_payments import (allocated_funds, unallocated_funds,
                                      check_brokers,
                                      allocate_funds_to_member_brokers,
                                      total_broker_stake)

from .model.leaves import (should_leaves, leaves,
                           decrement_allocated_funds_due_to_leaves,
                           increment_unallocated_funds_due_to_forfeit_stake,
                           decrement_total_stake_due_to_leaves)

from .model.joins import should_join, joins, increment_total_stake

from .model.helper_functions import count_brokers

from .model.claims import (should_make_claims, make_claims,
                           decrement_allocated_funds_by_claims)

from .mechanism import payment_to_unallocated, update_time_attached

from .behavior import payment_amt

psubs = [
    {
        'label': 'Update Time Attached',
        'policies': {

        },
        'variables': {
            'brokers': update_time_attached
        }
    },
    {
        'label': 'Payments',
        'policies': {
            'payment_amt': payment_amt
        },
        'variables': {
            'unallocated_funds': payment_to_unallocated
        },
        #                'total_funds': payment_to_total
        # random variable, flip a coin 0-10
    },
    {
        'label': 'Allocate Payments',
        'policies': {
            'check_brokers': check_brokers
        },
        'variables': {
            'allocated_funds': allocated_funds,     # A
            'unallocated_funds': unallocated_funds,   # R
            # 'total_funds': broker.deploy_agreement,         # F
            # 'committed_brokers': committed_brokers,   # B
            # each broker gets a share of allocated funds
            'brokers': allocate_funds_to_member_brokers,
            'total_broker_stake': total_broker_stake,  # S
            # 'horizon': ?,             # H
        }
    },
    {
        'label': 'Claims',
        'policies': {
            'should_make_claims': should_make_claims
        },
        "variables": {
            "brokers": make_claims,
            "allocated_funds": decrement_allocated_funds_by_claims
        },
    },
    {
        'label': 'Leaves',
        'policies': {
            'should_leaves': should_leaves
            },
        "variables": {
            "brokers": leaves,
            "allocated_funds": decrement_allocated_funds_due_to_leaves,
            "unallocated_funds": increment_unallocated_funds_due_to_forfeit_stake,
            "total_broker_stake": decrement_total_stake_due_to_leaves,
            "num_member_brokers": count_brokers
            }
    },
    {
        # if there's a vacant spot, flip a coin
        # (heads, they join, tails nobody joins)
        'label': 'Joins',
        'policies': {
            'should_join': should_join
            },
        "variables": {
            "brokers": joins,
            "num_member_brokers": count_brokers,
            "total_broker_stake": increment_total_stake
            },
    },
]
