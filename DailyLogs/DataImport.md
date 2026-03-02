## FixFinders: Data Import & Management Guide

This document explains how we populate the FixFinders Supabase production database with mock provider data, how to handle database constraints, and how to execute management commands when deploying on Render's free tier (which lacks Shell access).

### Overview

To ensure our FixFinders application has the necessary data for testing and development, we use a structured data import process. This involves generating mock provider data, handling database constraints, and utilizing management commands to populate the database effectively.

### 1. Data Import Process

Generating Mock Data:

- We use a Python script to generate mock provider data. This script creates realistic entries for providers, including names, contact information, and service details.
- The generated data is saved in a JSON format, which can be easily imported into the Supabase database.

Importing Data into Supabase:
