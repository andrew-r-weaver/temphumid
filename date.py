from datetime import datetime

def main():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    print(date_time)

if __name__ == "__main__":
    main()