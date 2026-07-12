# 🚀 AssetFlow - Enterprise Asset & Resource Management System

<div align="center">

![Odoo](https://img.shields.io/badge/Odoo-Hackathon-875A7B?style=for-the-badge&logo=odoo)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Status](https://img.shields.io/badge/Status-In%20Development-success?style=for-the-badge)

</div>

---

## 📌 Overview

AssetFlow is an **Enterprise Asset & Resource Management System** being developed as part of the **Odoo Hackathon**.

The system helps organizations efficiently manage physical assets, shared resources, maintenance workflows, employee allocations, and audit processes through a centralized ERP platform.

The project follows Odoo's modular ERP architecture with role-based access control, business workflows, approval mechanisms, dashboards, and reporting.

---

# 🎯 Objectives

- Digitize asset management
- Track complete asset lifecycle
- Prevent double allocation
- Manage resource booking
- Maintenance approval workflow
- Audit management
- Notifications & activity logs
- Dashboard & analytics

---

# 👥 User Roles

## Admin

- Manage departments
- Manage asset categories
- Manage employees
- Assign roles
- View organization reports

---

## Asset Manager

- Register assets
- Allocate assets
- Approve transfers
- Approve maintenance requests
- Manage returns

---

## Department Head

- Approve department allocations
- View department assets
- Book shared resources

---

## Employee

- View assigned assets
- Book resources
- Raise maintenance requests
- Initiate return & transfer requests

---

# ✨ Core Features

## Authentication

- Secure Login
- Role Based Access Control (RBAC)

---

## Organization Management

- Departments
- Employees
- Asset Categories

---

## Asset Management

- Asset Registration
- Auto Asset Tag Generation
- QR Code Support
- Asset Lifecycle Tracking

Asset Status:

- Available
- Allocated
- Reserved
- Under Maintenance
- Lost
- Retired
- Disposed

---

## Asset Allocation

- Allocate assets to employees
- Prevent double allocation
- Transfer workflow
- Return workflow
- Overdue tracking

---

## Resource Booking

- Shared rooms
- Equipment booking
- Vehicle booking

Features

- Calendar View
- Conflict Detection
- Time Slot Validation

---

## Maintenance Management

Workflow

Pending

↓

Approved

↓

Technician Assigned

↓

In Progress

↓

Resolved

---

## Audit Management

- Audit Cycles
- Auditor Assignment
- Discrepancy Reports
- Missing Asset Tracking

---

## Dashboard

KPIs

- Assets Available
- Assets Allocated
- Maintenance Today
- Active Bookings
- Pending Transfers
- Overdue Returns

---

## Reports

- Asset Utilization
- Maintenance Reports
- Department Reports
- Booking Reports

---

# 🏗️ Planned Architecture

```
AssetFlow

├── Authentication
├── Departments
├── Employees
├── Asset Categories
├── Assets
├── Allocation
├── Transfers
├── Resource Booking
├── Maintenance
├── Audit
├── Notifications
└── Dashboard
```

---

# 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| ERP Framework | Odoo Community |
| Language | Python |
| Database | PostgreSQL |
| ORM | Odoo ORM |
| UI | XML Views |
| Security | Odoo Access Control |

---

# 📂 Planned Module Structure

```
assetflow/

models/
views/
security/
data/
static/

__manifest__.py
__init__.py
```

---

# 🚧 Development Roadmap

- [x] Project Initialization
- [x] GitHub Repository Setup
- [ ] Odoo Module Setup
- [ ] Authentication
- [ ] Departments
- [ ] Employees
- [ ] Asset Categories
- [ ] Asset Registration
- [ ] Asset Allocation
- [ ] Resource Booking
- [ ] Maintenance Workflow
- [ ] Audit Management
- [ ] Dashboard
- [ ] Reports
- [ ] Testing
- [ ] Final Demo

---

# 📋 Business Rules

- Assets cannot be allocated to multiple users simultaneously.
- Booking conflicts are automatically prevented.
- Maintenance requests require approval before work begins.
- Returned assets automatically become available.
- Overdue assets are highlighted on the dashboard.
- Every action is logged for auditing purposes.

---



# 🏆 Odoo Hackathon

This repository contains our solution for the Odoo Hackathon problem statement **AssetFlow - Enterprise Asset & Resource Management System**.

The project is focused on demonstrating ERP architecture, modular design, secure role-based workflows, reusable business logic, and an intuitive user experience using the Odoo framework.

---

## ⭐ Current Status

🚧 Under Active Development
