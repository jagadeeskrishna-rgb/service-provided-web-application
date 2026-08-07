# service-provided-web-application
The Service Provided Web Application is a Django-based academic web application for on-demand home services and blue-collar gig economy support. It connects customers who need home services with local providers such as plumbers, electricians, cleaners, painters, appliance repair workers, AC repair technicians, and general labour workers. Customers can register, browse service categories, create booking requests, track status, submit mandatory feedback after completed bookings, and raise complaint/support tickets to admin. Service providers can register, create profiles, select multiple service types, accept available bookings after admin approval, update job progress, and upload completion or cancellation photos. Admin users can monitor customers, providers, bookings, reviews, service categories, support tickets, and provider approval status; they can approve/block provider signup requests, block providers at any time, reassign bookings from one provider to another, resolve customer tickets, and add/edit/remove service types.
The latest version strengthens the admin dashboard by adding complete monitoring views for customers, providers, bookings, reviews, services, and support tickets. It also introduces provider approval and blocking, booking reassignment, multi-service provider profiles, provider photo uploads, customer complaint tickets, and mandatory one-time feedback for completed bookings.

## Problem Statement
Customers often struggle to find reliable workers during urgent situations, while providers struggle to receive regular work. The absence of structured status tracking makes it difficult to know whether a request has been accepted, started, completed, cancelled, or escalated through a complaint.

## Proposed Solution
The project objectives are to provide role-based authentication, service category management, provider approval, multi-service provider profiles, service booking, status tracking, admin reassignment, support tickets, photo evidence, and forced one-time feedback after completion.

## Introduction
Local service booking still depends heavily on phone calls, personal references, and informal communication. This creates a gap between customers who need quick assistance and skilled workers who need reliable job opportunities.
The Service Provided Web Application addresses this gap through a structured Django web platform for home services such as plumbing, electrical repair, cleaning, painting, AC repair, appliance repair, and general labour support.
The application supports three major roles. Customers request work and track service progress. Service providers create profiles and handle jobs after admin approval. Admin users monitor the entire platform, manage service types, approve or block providers, reassign jobs, and resolve customer tickets.

|**Actor**       |**Main Responsibility**|
|----------------|-----------------------|
|Customer        |Register, browse services, create bookings, cancel eligible bookings, submit mandatory feedback, and raise support tickets.|
|Service Provider|Register, select multiple services, wait for approval, accept matching jobs, update status, and upload service photos.|
|Admin           |View all operational details, manage services, approve/block providers, reassign bookings, resolve tickets, and supervise reviews.|

