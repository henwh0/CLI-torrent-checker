""" Script intended to grab QBT download status and print to MOTD """

""" TODO: import correct libraries --> get connection info --> authenticate? --> format dl speed & format time?? --> grab and print torrent names and statuses --> make it look pretty --> ? """

import qbittorrentapi

connection_info = dict (
    host='YOUR HOSTNAME',
    username='YOUR WEBUI USERNAME',
    password='YOUR WEBUI PASSWORD'
)

def format_eta(seconds):
    if seconds < 0:
        return "∞"
    if seconds == 0:
        return "Done"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


try:
    client = qbittorrentapi.Client(**connection_info)
    client.auth_log_in()
    
    print("\n--- Torrent_Status ---")
    print(f"\nqBittorrent version: {client.app.version}\n")
    
    torrents = client.torrents_info()
    
    if not torrents:
        print("No active torrents")
    else:
        print(f"{'Name':<40} | {'Status':<12} | {'Progress':<8} | {'DL Speed':<12} | {'ETA':<10}")
        print("-" * 93)
        
        for t in torrents:
            name = (t.name[:37] + '..') if len(t.name) > 37 else t.name
            speed_mb = t.dlspeed / (1024 * 1024)
            readable_eta = format_eta(t.eta)
            print(f"{name:<40} | {t.state:<12} | {t.progress*100:>7.1f}% | {speed_mb:<7.2f} MB/s | {readable_eta:<10}")
            
except Exception as e:
    print(f"Error connecting to qBittorrent: {e}")