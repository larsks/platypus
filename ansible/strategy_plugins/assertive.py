from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.six.moves import reduce
from ansible.plugins.strategy.linear import StrategyModule as LinearStrategyModule

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class StrategyModule(LinearStrategyModule):
    def mark_host_failed(self, host):
        display.debug('LOOK MA NO HANDS')
        return super(StrategyModule, self).mark_host_failed(host)

    def _process_pending_results(self, iterator, one_pass=False,
                                 max_passes=None):

        for res in self._results:
            if res._task_fields.get('action') == 'assert':
                if res.is_failed():
                    res._result['failed'] = False
                    res._result['changed'] = True
                    res._result['ansible_stats'] = {
                        'data': {
                            'failed_assertions': 1,
                            'assertions': 1,
                        },
                        'per_host': False,
                        'aggregate': True,
                    }
                else:
                    res._result['ansible_stats'] = {
                        'data': {
                            'passed_assertions': 1,
                            'assertions': 1,
                        },
                        'per_host': False,
                        'aggregate': True,
                    }

        res = super(StrategyModule, self)._process_pending_results(iterator, one_pass, max_passes)


        return res
