.PHONY: all plots clean

all:    netids-fc.txt netids-cms.txt \
	adds.txt drops.txt \
	adds-cfs.txt drops-cfs.txt

# -- Generate data file and self-assessment plots for HW0

hw0.yml: hw0walk.py
	python hw0walk.py

plots: hw0.yml hw0plot.py
	python hw0plot.py


# -- Generate enrollment lists from FacultyCenter + CMS and reconcile

netids-fc.txt: ps.xls scrape_fc.py
	python scrape_fc.py

netids-cms.txt: CS_5220_student_table.csv scrape_cms.py
	python scrape_cms.py

adds.txt: netids-fc.txt netids-cms.txt
	diff -u netids-cms.txt netids-fc.txt | \
		grep -- "^+[a-z]" | sed 's/+//g' > adds.txt

drops.txt: netids-fc.txt netids-cms.txt
	diff -u netids-cms.txt netids-fc.txt | \
		grep -- "^-[a-z]" | sed 's/-//g' > drops.txt

netids-cfs.txt: netids-fc.txt
	awk '{ print $$1 "@cornell.edu;" }' \
		netids-fc.txt netids-ta.txt | sort > netids-cfs.txt

adds-cfs.txt: adds.txt
	awk '{ print $$1 "@cornell.edu;" }' adds.txt > adds-cfs.txt

drops-cfs.txt: adds.txt
	awk '{ print $$1 "@cornell.edu;" }' drops.txt > drops-cfs.txt


# -- Cleanup

clean:
	rm -f adds.txt drops.txt adds-cfs.txt drops-cfs.txt
	rm -f hw0-*.pdf

distclean:
	rm -f netids-fc.txt netids-cms.txt hw0.yml 
	rm -f ps.xls CS_5220_student_table.csv
