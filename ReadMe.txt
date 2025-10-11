Key Engineering Practices Used
Principle	            Description
Modularity	            Logic, constants, and UI separated cleanly.
Single Responsibility	Each file does one job: constants, calculations, or UI.
Pure Functions	        zerodha_intraday_pnl() has no side effects, perfect for reuse or unit testing.
Validation	            Input validation with clear errors.
Scalability	            Easy to extend later (e.g., add delivery or F&O modules).
Maintainability 	    Constants centralized; logic readable and isolated.
OOP in GUI	            Class-based UI, encapsulating widget logic.
Best Practices	        PEP-8 style, type hints, descriptive names, layered architecture.