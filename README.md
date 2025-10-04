# Travelex-Rate
FX Rate Tracker: Python ETL to Fun
What This Does (Project Goal)

Simple: Get Exchange rate from the webpage
As a expat just curious about when to order FX and when is sales in place.
The output data is clean, ready for Power BI or other tools.

    Python

    Selenium

    Pandas

How the Script Works (ETL Steps)

    Extract: Python uses Selenium. Clcik buttons and abstract real time rate from a provider.

    Transform: Puts all those rates into a table. Adds date and the amount of testing

    Load: Takes the clean table. Appends it to the casv file.

    Install requirements: See requirements.txt.

    ChromeDriver: need to be installed locally to make the script work.
