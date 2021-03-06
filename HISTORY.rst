Changelog
---------

0.15.0
~~~~~~

- Feature: steps (#221)
- Make activity task result optional (#225)
- Use details in addition to name to find markers (#227)
- Logging: add exception information (#163)
- swf/actors: support 'Message' key (#224)
- Implement markers (#216) (#217)
- Add retry on swf.process.Poller.poll and fail (#208)

0.14.2
~~~~~~

- propagate_attribute: skip signal objects (#215)
- Local executor: check add_activity_task (#215)

0.14.1
~~~~~~

- Don't send exception up if raises_on_failure is false (#213)
- Fix UnicodeDecodeError on windows machine (#211)
- Try to use less memory (#209)
- Standalone mode: use created task list for children activities (#207)

0.14.0
~~~~~~

- Fix workers not stopping in case they start during a shutdown (#205)
- Add support for SWF signals (#188)
- Improvements on canvas.Group (#204)

0.13.4
~~~~~~

- Implement metrology on SWF and local workflows (#186)

0.13.3
~~~~~~

- Try..except pass for NoSuchProcess (#182)

0.13.2
~~~~~~

- Add optional canvas (#193)
- Reorganize tests/ directory (#198)
- Relax DeciderPoller task list check (#201)
- Implement priorities on SWF tasks (#199)

0.13.1
~~~~~~

- Fix SWF executor not accepting ActivityTask's in submit() method (#196)

0.13.0
~~~~~~

- Implement child workflow (#74)
- Don't schedule idempotent tasks multiple times (#107)
- Child workflow ID: use parent's id to generate

0.12.7
~~~~~~

- Control SWF processes identity via environment (#184)

0.12.6
~~~~~~

- Replace ``execution`` object with a more flexible ``get_execution_method()`` (#177)
- Fix README_SWF.rst format (#175)
- Fix CONTRIBUTING.rst format
- docs/conf.py: remove relative import

0.12.5
~~~~~~

- Executor: expose workflow execution (#172)

0.12.4
~~~~~~

- Avoid returning too big responses to RespondDecisionTaskCompleted endpoint (#166)
- Worker: remove useless monitor_child (#168)

0.12.3
~~~~~~

- Add max_parallel option in Group (#164)

0.12.2
~~~~~~

- Make the dynamic dispatcher more flexible (#161)
- Fix README.rst format (#160)
- Tiny command-line usability fixes (#158)

0.12.1
~~~~~~

- Don't override passed "default" in json_dumps() (#155)
- Expose activity context (#156)

0.12.0
~~~~~~

- Improve process management (#142)

0.11.17
~~~~~~~

- Don't reap children in the back of multiprocessing (#141)
- Don't force to pass a workflow to activity workers (#133)
- Don't override the task list if not standalone (#139)
- Split FuncGroup submit (#146)
- CI: Test on python 3 (#144)
- Decider: use workflow's task list if unset (#148)

0.11.16
~~~~~~~

- Refactor: cleanups and many python 3 compatibility issues fixed (#135)
- Introduce AggregationException to inspect exceptions inside canvas.Group/Chain (#92)
- Improve heartbeating, now enabled by default on activity workers (#136)

0.11.15
~~~~~~~

- Fix tag_list declaration in case no tag is associated with the workflow
- Fix listing workflow tasks not handling "scheduled" (not started) tasks correctly
- Fix CSV formatter outputing an extra "None" at the end of the output
- Fix 'simpleflow activity.rerun' resolving the bad function name if not the last event

0.11.14
~~~~~~~

- Various little fixes around process management, heartbeat, logging (#110)

0.11.13
~~~~~~~

- Add ability to provide a 'run ID' with 'simpleflow standalone --repair'

0.11.12
~~~~~~~

- Fix --tags argument for simpleflow standalone (#114)
- Improve tests and add integration tests (#116)
- Add 'simpleflow activity.rerun' command (#117)

0.11.11
~~~~~~~

- Fix a circular import on simpleflow.swf.executor

0.11.10
~~~~~~~

- Fix previous_history initialization (#106)
- Improve WorkflowExecutionQueryset default date values (#111)

0.11.9
~~~~~~

- Add a --repair option to simpleflow standalone (#100)

0.11.8
~~~~~~

- Retry boto.swf connection to avoid frequent errors when using IAM roles (#99)

0.11.7
~~~~~~

Same as 0.11.6 but the 0.11.6 on pypi is broken (pushed something similar to 0.11.5 by mistake)

0.11.6
~~~~~~

- Add ``issubclass_`` method (#96)
- Avoid duplicate logs if root logger has an handler (#97)
- Allow passing SWF domain via the SWF_DOMAIN environment variable (#98)

0.11.5
~~~~~~

- Don't mask activity cancel exception (#84)
- Propagate all decision response attributes up to Executor.replay() (#76, #94)

0.11.4
~~~~~~

- ISO dates in workflow history #91
- Fix potential infinite retry loop #90

0.11.3
~~~~~~

- Fix replay hooks introduced in 0.11.2 (#86)
- Remove python3 compatibility from README (which was not working for a long time)

0.11.2
~~~~~~

- Add new workflow hooks (#79)

0.11.1
~~~~~~

- Fix logging when an exception occurs

0.11.0
~~~~~~

- Merge ``swf`` package into simplefow for easier maintenance.


0.10.4 and below
~~~~~~~~~~~~~~~~

Sorry changes were not documented for simpleflow <= 0.10.x.
