# System Drone


# this file implements System Drone
import time
import pprint
import traceback

from pheromones.pheromone import Pheromone


class Drone:
    def __init__(
            self,
            pheromone: Pheromone,
            console_mode=True,
            # **kwargs
    ):
        if pheromone.not_completed():
            raise AssertionError("pheromone is not complete, need modules: " + ', '.join(pheromone.need_to_be_filled()))

        self._inited = False  # if initializer should set it True before return.
        self._finished = False  # after clearer it should be set True so it won't run again.

        self._config = pheromone.config

        self._console_mode = pheromone.console_mode  # console mode should mute output.

        # journal is all about task information.
        self.journal = pheromone.journal
        self._config.save_path = self.journal.save_path or self._config.save_path
        self._config.save_pattern = self.journal.save_pattern or self._config.save_pattern
        self._config.interval_ = self.journal.interval or self._config.interval_

        # a stat reporting class, could be used to check working status on console.
        self._reporter = pheromone.reporter(self._config)

        # modules initializations.
        self._initializer = pheromone.initializer(self._config)
        self._downloader = pheromone.downloader(self._config)
        self._extractor = pheromone.extractor(self._config)
        self._file_manager = pheromone.file_manager(self._config)
        self._clearer = pheromone.clearer(self._config)

    def launch(self):
        if self._finished:
            return self, self._reporter.report(), None
        try:
            if not self._inited:
                # all modules communicate by journal, report by reporter, so no message queue.
                self._initializer.init(self.journal, self._reporter)
                self._inited = True

            self._start()

            self._clearer.clear(self.journal, self._reporter)
            self._finished = True
        except Exception as e:
            print("===============================")
            print(e)
            traceback.print_exc()
            print("===============================")
            if self._console_mode:
                print("oops, we've run into an exception.")
                input('press enter to see report...')
                traceback.print_exc()
            return self, self._reporter.report(), e
        else:
            # some print for standalone mode
            if self._console_mode:
                input('task finished.\npress enter to see report...')
                pprint.pprint(self._reporter.report())
            return self, self._reporter.report(), None

    def _start(self):
        while not self.journal.task_finished:
            # send request
            self._downloader.request(self.journal, self._reporter)

            # parsing any response
            self._extractor.extract(self.journal, self._reporter)

            # save content
            self._file_manager.save(self.journal, self._reporter)

            # take a little rest.
            time.sleep(self._config.interval())

    def report(self):
        return self._reporter.report()

    def finished(self):
        return self._finished
