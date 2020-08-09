from ftplib import FTP
import os
import errno
import config
exportList = []


class NasdaqController:
    def getList(self):
        return exportList

    def __init__(self, update=True):

        self.filenames = {
            "otherlisted": config.OTHER_LISTED_PATH,
            "nasdaqlisted": config.NASDAQ_LISTED_PATH
        }

        # Update lists only if update = True

        if config.UPDATE_STOCK_LIST:
            self.ftp = FTP("ftp.nasdaqtrader.com")
            self.ftp.login()

            #print("Nasdaq Controller: Welcome message: " + self.ftp.getwelcome())

            self.ftp.cwd("SymbolDirectory")

            for filename, filepath in self.filenames.items():
                if not os.path.exists(os.path.dirname(filepath)):
                    try:
                        os.makedirs(os.path.dirname(filepath))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                self.ftp.retrbinary("RETR " + filename +
                                    ".txt", open(filepath, 'wb').write)

        all_listed = open(config.PATH_TO_STOCK_LIST, 'w')
        all_tickers = []
        tickers_to_exclude = []

        with open(config.EXCLUDED_STOCK_PATH, "r") as file_reader_excluded:
            for j, line_excluded in enumerate(file_reader_excluded, 0):
                if j == 0:
                    continue
                line_split = line_excluded.strip().split("|")
                if line_split[0] == "":
                    continue
                tickers_to_exclude.append(line_split[0])
        print("Excluded tickers = " + str(len(tickers_to_exclude)))
        
        # Compile list of all tickers possible
        for filename, filepath in self.filenames.items():
            with open(filepath, "r") as file_reader:
                for i, line in enumerate(file_reader, 0):
                    if i == 0:
                        continue
                    line_split = line.strip().split("|")
                    if line_split[0] == "" or line_split[1] == "" or line[0] in tickers_to_exclude:
                        continue
                    all_tickers.append(line)
        # Compile list of tickers to exclude
       
        # Output all tickers - tickers to exclude
        for y in all_tickers:
            line = y.strip().split("|")
            if line[0] == "" or line[1] == "" or line[0] in tickers_to_exclude:
                continue
            all_listed.write(line[0] + ",")

            global exportList
            exportList.append(line[0])
            all_listed.write(line[0] + "|" + line[1] + "\n")
        