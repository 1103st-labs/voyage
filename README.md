# voyage

## What is voyage?
Voyage is a yet another todo system for those of us with executive functions
that are well... Lacking.

The system is best explained with an example:

Let's say you are a modern rennaissance person with a plethora of ongoing
interests. If, say, one of these interests happens to be chicken smuggling we
would note this in the voyage system as a *heading*. A heading in other terms is
just a direction you have chosen to go with in your life. In the case of
chicken smuggling, a poor choice. Nonetheless, the life of a poultry mule is an
eventful one; you will need to bag the birds, hide them in the seats of your
aging 2005 ford fiesta, and finally make the drive across the Spanish-Portuguese
border. Each of these tasks would be considered *waypoints* in the overarching
chicken smuggling *heading*. A waypoint is a specific, actionable task that can
be preferably taken care of in one sitting. Just saying "move the birds from
Madrid to Averio" is too vague for a waypoint. In some ways a waypoint is kinda
like a S.M.A.R.T. goal. 

It's a very simple setup with only two objects, *waypoint* and *heading*. This
is intentional. Voyage is designed to be as simple to maintain and deal with
from a mental energy standpoint as possible. 

In the above low energy spirit, voyage systems are coded so that waypoints may
be added automatically whenever possible. This is achieved by a standardized
waypoint object and the sync.py file. Currently supported sync methods are
listed below:
- ical via add_ical(...)

More will be added and since everything is in python it's very easy to fit into
whatever workflow.

## How do I use it?
The core voyage system can be applied in may ways and hopefully many will be
developed.

As of right now there are two interfaces available:
1. Discord - The code for a discord bot can be found in the main branch. It works technically but is very much a pre-alpha.
2. Google Keep - See the keep branch for more info. This is the recommended
   interface for right now.
