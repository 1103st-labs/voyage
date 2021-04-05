import gkeepapi as keep
import time
import argparse
import sync
import importlib
import datetime
# hints
# import waypoint_def as way; manifest = [way.Waypoint() for x in range(10)]
# Parse args
parser = argparse.ArgumentParser(description='A manifest based TODO System.')
parser.add_argument('email', metavar='E', help='The user email.')
parser.add_argument('pas', metavar='P', help='The app password.')
parser.add_argument('-n', help='Clear Waypoints and exit.',
                    action='store_true')
args = vars(parser.parse_args())
# Login to keep
k = keep.Keep()
k.login(args["email"], args["pas"])
print("INFO: LOGED IN.")
# TODO Cashing...
# set up keep
k.findLabel("MANIFEST", create=True)
k.findLabel("ADVISED", create=True)
k.findLabel("LIMBO", create=True)
k.findLabel("DONE", create=True)
k.sync()
# Main Sync Loop
while(True):
    try:
        k.sync()
        old_time = datetime.datetime.now()
        # Generate old and new headings
        importlib.reload(sync)
        headings = {x: k.findLabel(x, create=True) for x in sync.HEADINGS}
        old_manifest = list(k.find(labels=[k.findLabel("WAYPOINT", create=True)]))
        if (args["n"]):
            [x.delete() for x in old_manifest]
            k.sync()
            print("INFO: Cleared waypoints....")
            exit(0)
        manifest = sync.gen_manifest()
        old_content = {x: x.text.split("\n") for x in old_manifest}
        old_hash = {old_content[x][-1]: x for x in old_manifest}
        synced = {}
        # sync
        for w in manifest:
            if (w.hash in old_hash.keys()):
                if (datetime.datetime.now() > (datetime.timedelta(seconds=30) + old_time)):
                    k.sync()
                    old_time = datetime.datetime.now()
                old = old_hash[w.hash]
                if (old.archived):
                    if not(old.labels.get(k.findLabel("DONE", create=True))):
                        old.labels.add(k.findLabel("DONE", create=True))
                        old_time = datetime.datetime.now()
                        k.sync()
                else:
                    old.text = w.gen_sum()
                    synced[old] = w
            else:
                new = k.createNote(w.des, w.gen_sum())
                new.labels.add(headings[w.heading])
                new.labels.add(k.findLabel("WAYPOINT", create=True))
                synced[new] = w
        # Clean out old / removed waypoints
        to_limbo = [x for x in old_manifest 
                    if (x not in synced.keys())
                    and not(x.labels.get(k.findLabel("DONE", create=True)))]
        for x in to_limbo:
            x.pinned = False
            x.archived = True
            x.labels.add(k.findLabel("LIMBO", create=True))
        # Mark levels of attention
        ordered = list(synced.values())
        ordered.sort(key=lambda x: time.mktime(x.due.timetuple()))
        now = datetime.datetime.now(sync.LOCAL_TIMEZONE)
        for x in synced:
            if (x.labels.get(k.findLabel("MANDATORY", create=True))):
                x.labels.remove(k.findLabel("MANDATORY", create=True))
            if (x.labels.get(k.findLabel("ADVISED", create=True))):
                x.labels.remove(k.findLabel("ADVISED", create=True))
            # The unDONE mechanism
            if (x.labels.get(k.findLabel("DONE", create=True))):
                x.labels.remove(k.findLabel("DONE", create=True))
            x.pinned = False
        for x in ordered:
            if (now > (x.due - datetime.timedelta(minutes=x.dur))):
                vis = [xx for xx, yy in synced.items() if yy == x][0]
                vis.pinned = True
                vis.color = keep.node.ColorValue.Red
                vis.labels.add(k.findLabel("MANDATORY", create=True))
            elif (now > (x.due - datetime.timedelta(days=1))):
                vis = [xx for xx, yy in synced.items() if yy == x][0]
                vis.pinned = True
                vis.color = keep.node.ColorValue.Orange
                vis.labels.add(k.findLabel("MANDATORY", create=True))
            elif (now > (x.due - datetime.timedelta(days=x.a_time))):
                vis = [xx for xx, yy in synced.items() if yy == x][0]
                vis.pinned = True
                vis.color = keep.node.ColorValue.Yellow
                vis.labels.add(k.findLabel("ADVISED", create=True))
            else:
                vis = [xx for xx, yy in synced.items() if yy == x][0]
                vis.pinned = False
                vis.color = keep.node.ColorValue.Gray
        k.sync()
        print(f'INFO: Sync run at {time.asctime()}')
        time.sleep(sync.SYNC_SLEEP)
    except keep.exception.APIException as e:
        print(e)
        print('ERR: Keep api had a stroke....')
        pass
   # except exception.APIException as e:
   #     print(e)
   #     time.sleep(60 * 10)
   #     print('ERR: Keep api had a stroke....')
   #     pass
