from manager.torrent_manager import TorrentManager

if __name__ == "__main__":
    manager = TorrentManager()
    stats = manager.process_torrents()
    print(f"Results: {stats}")
