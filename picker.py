#!/usr/bin/env python

"""
Pick on students for in-class work
"""

import yaml
import random
import heapq
from tkinter import Tk, Frame, Button, Label, LEFT, BOTH
from datetime import date


class ClassCheck(object):
    """Represent in-class answering checklist.

    The ClassCheck list maintains a priority queue for students to
    answer questions.  Students who have answered fewer past questions
    (e.g. because of absence) get higher priority.  Within a priority
    level, the order is determined by a random shuffle at the start of
    the class.

    NB: Only students that are enrolled are listed.
    """

    def __init__(self, recs, inclass):
        """Initialize the checklist.

        Args:
            recs: List of student records from HW0
            inclass: In-class participation checklist
        """
        self._name = {}
        self._queue = []
        self.inclass = inclass
        random.shuffle(recs)
        for rec in recs:
            if 'drop' not in rec and rec['status'] == 'enrolled':
                netid = rec['netid']
                count = len(inclass[netid]) if netid in inclass else 0
                entry = (count, len(recs), netid)
                self._name[netid] = rec['name'] if 'name' in rec else netid
                heapq.heappush(self._queue, entry)
        self._choice = heapq.heappop(self._queue)

    def choice(self):
        "Return the netid of the most recent choice"
        return self._choice[2]

    def name(self):
        "Return the name and netid of the most recent choice"
        netid = self.choice()
        return "{0} ({1})".format(self._name[netid], netid)
    
    def mark_none(self):
        "Mark current choice as absent (don't pick again this time)"
        self.pick(False)

    def mark_pass(self):
        "Mark current choice as having passed on a question"
        self.mark("pass")
        self.pick()

    def mark_okay(self):
        "Mark current choice as attempting a question"
        self.mark("okay")
        self.pick()

    def mark(self, stamp):
        """Register an attempt at a question
        
        Args:
            stamp: Text string describing response type
        """
        netid = self.choice()
        if netid not in self.inclass:
            self.inclass[netid] = []
        self.inclass[netid].append({'date': date.today().isoformat(),
                                    'type': stamp})

    def pick(self, present=True):
        "Record the current data and pick the next person"
        if present:
            entry = (self._choice[0] + 1, self._choice[1], self._choice[2])
            heapq.heappush(self._queue, entry)
        self._choice = heapq.heappop(self._queue)


class PickerGUI(Frame):
    """Tkinter GUI for picking on students enrolled in the class.
    """
    
    def __init__(self, parent, recs, inclass):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.checklist = ClassCheck(recs, inclass)
        self.initUI()

    def set_text(self, text):
        self.label['text'] = text

    def pick(self):
        self.set_text(self.checklist.name())

    def reply_none(self):
        self.checklist.mark_none()
        self.pick()

    def reply_pass(self):
        self.checklist.mark_pass()
        self.pick()

    def reply_try(self):
        self.checklist.mark_okay()
        self.pick()

    def reply_done(self):
        self.checklist.mark_okay()
        self.set_text("")

    def initUI(self):
        self.parent.title("Picker")
        b1 = Button(self, text="Pick",   command=self.pick)
        b2 = Button(self, text="Silent", command=self.reply_none)
        b3 = Button(self, text="Pass",   command=self.reply_pass)
        b4 = Button(self, text="Try",    command=self.reply_try)
        b4 = Button(self, text="Done",   command=self.reply_done)
        b5 = Button(self, text="Quit",   command=self.quit)
        b1.pack(side=LEFT)
        b2.pack(side=LEFT)
        b3.pack(side=LEFT)
        b4.pack(side=LEFT)
        b5.pack(side=LEFT)        
        self.label = Label(self.parent, text="", font=("Helvetica",24))
        self.label.pack(fill=BOTH, expand=1)
        self.pack()


def main():
    with open("hw0.yml", "r") as f:
        recs = yaml.load(f)
    with open("inclass.yml", "r") as f:
        inclass = yaml.load(f)
        if inclass is None:
            inclass = {}

    root = Tk()
    root.geometry("250x150+300+300")
    app = PickerGUI(root, recs, inclass)
    root.mainloop()

    with open("inclass.yml", "w") as f:
        f.write(yaml.dump(inclass, default_flow_style=False))


if __name__ == "__main__":
    main()
