<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Trip Finance Telegram Bot</h3>

  <p align="center">
    Easily manage your group finance during a trip!
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#how-it-works">How It Works</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

I was in charge of managing my group's finance during an oversea trip. I faced difficulties with tabulating how much each person spent and having to update the finance googlesheet.
I built this bot to streamline the process and made the googlesheet update automatically.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Here is how the code works:

### Prerequisites

These some libraries used for the project:

* python-telegram-bot
  ```sh
  pip install python-telegram-bot
  ```
* gspread
  ```sh
  pip install gspread
  ```
* dotenv
  ```sh
  pip install python-dotenv
  ```

<!-- How it works -->
## How it works

* Telegram bot sends a menu message when promted with "/start" command
  ![alt text][Menu]

* /Deduct:
    Sends a receipt to telegram bot and it will deduct the amount from each person's column in googlesheet
* /Deposit:
    Sends a receipt to telegram bot and it will add the amount from each person's column in googlesheet
* /Balance:
    Bot will send the balance of each person from googlesheet
* /Excel:
    Bot sends the googlesheet link
* /End:
    Ends session

* Receipt example

    Event Title
    Person 1 : $
    Person 2 : $
    Person x : $

    Total : $

* Googlesheet:

![alt text][Googlesheet]

    New receipt will be added onto a new row from row 7 onwards.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Googlesheet]: https://github.com/JamesTzh/Trip_Finance_Telegram_Bot/blob/main/Googlesheet%20Template.png
[Menu]: https://github.com/JamesTzh/Trip_Finance_Telegram_Bot/blob/main/Menu.png
