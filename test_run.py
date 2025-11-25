from manager.torrent_manager import TorrentManager

if __name__ == "__main__":
    manager = TorrentManager(dry_run=True)
    stats = manager.process_torrents()
    print(f"Results: {stats}")
