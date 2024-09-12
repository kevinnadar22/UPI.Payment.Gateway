
## UPI Payment Gateway API

<p align="center">

![Fork](https://img.shields.io/github/forks/kevinnadar22/UPI.Payment.Gateway?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/kevinnadar22/UPI.Payment.Gateway?color=%23&style=for-the-badge)
![License](https://img.shields.io/github/license/kevinnadar22/UPI.Payment.Gateway?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/kevinnadar22/UPI.Payment.Gateway?style=for-the-badge)

</p>
  <p align="center">
    UPI Payment Gateway API
    <br />
    ·
    <a href="https://www.telegram.dog/ask_admin001">Report Bug</a>
    ·
    <a href="#key-features">Features</a>
    ·
    <a href="#deploy">Deploy</a>
    ·
    <a href="#required-variables">Variables</a>
  </p>
</div>

## Table of Contents

- [Overview](#overview)
  - [Tutorial](#tutorial)
  - [API Reference](#api-reference)
  - [Key Features](#key-features)
  - [Use Cases](#use-cases)
  - [Problem](#problem)
  - [Solution](#solution)
  - [Required Variables](#required-variables)
  - [Deployment Options](#deployment-options)
  - [Stack Used](#stack-used)

### Tutorial

For a step-by-step guide on setting up and using the UPI Payment Gateway API, please refer to the following tutorial: [YouTube Tutorial](https://www.youtube.com/watch?v=dummy_link)

### API Reference

[API Documentation](API_README.md)

### Overview

The UPI Payment Gateway API is designed to log and track UPI transactions by UPI Reference ID. This API can be integrated as a payment gateway in your website, app, or any other platform to track UPI payments. It provides a simple and efficient way to manage UPI transactions without the need for complex payment gateways.

### Key Features

- **Transaction Status Tracking**: Track the status of UPI transactions, including credited or debited status by UPI reference ID.

### Use Cases

- **Payment Gateway Integration**: Integrate the API as a payment gateway in your website or app to track UPI transactions.
- **Subscription Management**: Manage subscriptions and payments by tracking UPI transactions.

### Problem

Payment gateways often require users to provide detailed business information, which can be cumbersome for individual users who simply want to integrate a subscription or payment system in their small business or personal website. Additionally, tracking UPI transactions can be challenging, as users need to manually log each transaction, which can be time-consuming and error-prone.

### Solution

Users can connect their message apps on Android devices or set up a shortcut on iOS devices to automatically forward UPI transaction messages to our API. The API then processes these messages to log crucial payment information, including UPI reference, UPI ID, credited or debited status, and transaction amount.

Once the API is set up, UPI QR codes can be generated for customers to scan and make payments. Customers should enter the UPI reference ID, and the API can track the payment status.


### Required Variables

| Variable Name              | Value                                                                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DATABASE_URL` (required)  | [mongoDB](https://www.mongodb.com) URI. Get this value from [mongoDB](https://www.mongodb.com). |
| `DATABASE_NAME` (optional) | Name of the database in [mongoDB](https://www.mongodb.com).                                    |

### Deployment Options

You can deploy this bot anywhere. Below are some recommended options:

|                                                        | Name                 | Deploy                                                                                                                                                                                                                             |
| ------------------------------------------------------ | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![Heroku](assets/heroku.png)](https://heroku.com) | Heroku               | [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2Fkevinnadar22%2FUPI.Payment.Gateway)                                                                                    |
| ![Koyeb](assets/koyeb.png)                         | Koyeb                | [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/services/deploy?type=git&builder=dockerfile&repository=github.com/kevinnadar22/UPI.Payment.Gateway&branch=main&env[FLASK_ENV]=production&env[DATABASE_URL]=YOUR_DATABASE_URL) |
                                                                                                                                                                                                  
### Stack Used

- **Flask**: For building the API
- **Python**: Version 3.10.6