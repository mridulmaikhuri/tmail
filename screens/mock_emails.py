mock_emails = [
    {
        "id": "1",
        "sender": "github@notifications.com",
        "subject": "New pull request opened in your repository",
        "date": "2026-02-20 09:14",
        "snippet": "A contributor opened a pull request in your project.",
        "body": """
        Hello Mridul,

        A new pull request has been opened in your repository:

        Repository: terminal-mail-client
        Title: Add OAuth authentication flow

        Please review the changes and merge if appropriate.

        You can view the pull request here:
        https://github.com/example/repo/pull/42

        Best,
        GitHub Notifications
        """,
        "link": "https://mail.google.com/mail/u/0/#inbox/19d2e07df1c65f56",
        "attachments": [{
            'filename': 'Notice.pdf', 'mimeType': 'application/pdf', 
            'attachmentId': 
            'ANGjdJ9A5vYScaYCAL5hG8owLEY8Hlb2BatRY2cgo9M96YQNKCAhFYy_m1ACKUSpPBVK7R6-YHplY4nxH0YApc-T3vS87r9g_hDv9TDqobmKoJEbB3UZUmJZtZSgTOeLQipXGpwfeu62C2lE2NfX5ENdnasLO0zAPZL3mR2DNwklqimFOElg-2h_YeDwrSF82Z8oqRhpSrk4-yV0mXrBTp2DRxxKmIsJTkmTt6FGOOevAV-GMTEiTb6x5VhUEweC8IbQBFARzQpmCMkQhVw9MWeOCPWA6KDdNR7lpeCWGCXNQY-ZaD4T-Wk8XpAAPPkYG7uuvldU62LjcoyBf8-DCLDQioI8SLhkkRqdOD6fA0_6du6JKiAXK9dbnbuC3ct2T5hdV3wQHDxZecD7xbPv'
        }]
    },

    {
        "id": "2",
        "sender": "noreply@codeforces.com",
        "subject": "Your Codeforces contest rating has been updated",
        "date": "2026-02-18 22:05",
        "snippet": "Your rating has changed after Codeforces Round #1079.",
        "body": """
        Hello Mridul,

        Your rating has been updated after Codeforces Round #1079.

        Previous Rating: 1412
        New Rating: 1478
        Rank: Specialist

        Congratulations on your performance!

        Keep practicing and participating in contests.

        Codeforces Team
        """,
        "link": "https://mail.google.com/mail/u/0/#inbox/19d2e07df1c65f56",
        "attachments": [{
            'filename': 'Notice.pdf', 'mimeType': 'application/pdf', 
            'attachmentId': 
            'ANGjdJ9A5vYScaYCAL5hG8owLEY8Hlb2BatRY2cgo9M96YQNKCAhFYy_m1ACKUSpPBVK7R6-YHplY4nxH0YApc-T3vS87r9g_hDv9TDqobmKoJEbB3UZUmJZtZSgTOeLQipXGpwfeu62C2lE2NfX5ENdnasLO0zAPZL3mR2DNwklqimFOElg-2h_YeDwrSF82Z8oqRhpSrk4-yV0mXrBTp2DRxxKmIsJTkmTt6FGOOevAV-GMTEiTb6x5VhUEweC8IbQBFARzQpmCMkQhVw9MWeOCPWA6KDdNR7lpeCWGCXNQY-ZaD4T-Wk8XpAAPPkYG7uuvldU62LjcoyBf8-DCLDQioI8SLhkkRqdOD6fA0_6du6JKiAXK9dbnbuC3ct2T5hdV3wQHDxZecD7xbPv'
        }]
    },

    {
        "id": "3",
        "sender": "alerts@bank.com",
        "subject": "Transaction Alert: ₹4,500 debited",
        "date": "2026-02-17 14:12",
        "snippet": "Your account was debited for a recent purchase.",
        "body": """
        Dear Customer,

        A transaction of ₹4,500 has been debited from your account.

        Merchant: Amazon India
        Date: 17 Feb 2026
        Time: 14:10 IST

        If this transaction was not performed by you, please contact
        our support immediately.

        Thank you,
        SecureBank
        """,
        "link": "https://mail.google.com/mail/u/0/#inbox/19d2e07df1c65f56",
        "attachments": [{
            'filename': 'Notice.pdf', 'mimeType': 'application/pdf', 
            'attachmentId': 
            'ANGjdJ9A5vYScaYCAL5hG8owLEY8Hlb2BatRY2cgo9M96YQNKCAhFYy_m1ACKUSpPBVK7R6-YHplY4nxH0YApc-T3vS87r9g_hDv9TDqobmKoJEbB3UZUmJZtZSgTOeLQipXGpwfeu62C2lE2NfX5ENdnasLO0zAPZL3mR2DNwklqimFOElg-2h_YeDwrSF82Z8oqRhpSrk4-yV0mXrBTp2DRxxKmIsJTkmTt6FGOOevAV-GMTEiTb6x5VhUEweC8IbQBFARzQpmCMkQhVw9MWeOCPWA6KDdNR7lpeCWGCXNQY-ZaD4T-Wk8XpAAPPkYG7uuvldU62LjcoyBf8-DCLDQioI8SLhkkRqdOD6fA0_6du6JKiAXK9dbnbuC3ct2T5hdV3wQHDxZecD7xbPv'
        }]
    },

    {
        "id": "4",
        "sender": "newsletter@techweekly.com",
        "subject": "Top Programming Trends in 2026",
        "date": "2026-02-16 08:30",
        "snippet": "AI engineering, Rust adoption, and edge computing.",
        "body": """
        Hello Subscriber,

        Here are the top programming trends this week:

        1. AI-powered developer tools
        2. Rust adoption in system-level programming
        3. Rise of edge computing
        4. Terminal-based developer tools

        Read the full article here:
        https://techweekly.com/articles/programming-trends-2026

        TechWeekly Team
        """,
        "link": "https://mail.google.com/mail/u/0/#inbox/19d2e07df1c65f56",
        "attachments": [{
            'filename': 'Notice.pdf', 'mimeType': 'application/pdf', 
            'attachmentId': 
            'ANGjdJ9A5vYScaYCAL5hG8owLEY8Hlb2BatRY2cgo9M96YQNKCAhFYy_m1ACKUSpPBVK7R6-YHplY4nxH0YApc-T3vS87r9g_hDv9TDqobmKoJEbB3UZUmJZtZSgTOeLQipXGpwfeu62C2lE2NfX5ENdnasLO0zAPZL3mR2DNwklqimFOElg-2h_YeDwrSF82Z8oqRhpSrk4-yV0mXrBTp2DRxxKmIsJTkmTt6FGOOevAV-GMTEiTb6x5VhUEweC8IbQBFARzQpmCMkQhVw9MWeOCPWA6KDdNR7lpeCWGCXNQY-ZaD4T-Wk8XpAAPPkYG7uuvldU62LjcoyBf8-DCLDQioI8SLhkkRqdOD6fA0_6du6JKiAXK9dbnbuC3ct2T5hdV3wQHDxZecD7xbPv'
        }]
    },

    {
        "id": "5",
        "sender": "team@university.edu",
        "subject": "Machine Learning Project Submission Reminder",
        "date": "2026-02-15 19:45",
        "snippet": "Reminder: Submit your SDN routing ML project.",
        "body": """
        Dear Student,

        This is a reminder that your project submission deadline is approaching.

        Project Title:
        Machine Learning-Based Routing in Software Defined Networks

        Deadline:
        25 February 2026

        Please upload your project report and code repository before
        the deadline.

        Best regards,
        Department of Computer Science
        """,
        "link": "https://mail.google.com/mail/u/0/#inbox/19d2e07df1c65f56",
        "attachments": [{
            'filename': 'Notice.pdf', 'mimeType': 'application/pdf', 
            'attachmentId': 
            'ANGjdJ9A5vYScaYCAL5hG8owLEY8Hlb2BatRY2cgo9M96YQNKCAhFYy_m1ACKUSpPBVK7R6-YHplY4nxH0YApc-T3vS87r9g_hDv9TDqobmKoJEbB3UZUmJZtZSgTOeLQipXGpwfeu62C2lE2NfX5ENdnasLO0zAPZL3mR2DNwklqimFOElg-2h_YeDwrSF82Z8oqRhpSrk4-yV0mXrBTp2DRxxKmIsJTkmTt6FGOOevAV-GMTEiTb6x5VhUEweC8IbQBFARzQpmCMkQhVw9MWeOCPWA6KDdNR7lpeCWGCXNQY-ZaD4T-Wk8XpAAPPkYG7uuvldU62LjcoyBf8-DCLDQioI8SLhkkRqdOD6fA0_6du6JKiAXK9dbnbuC3ct2T5hdV3wQHDxZecD7xbPv'
        }]
    }
]
