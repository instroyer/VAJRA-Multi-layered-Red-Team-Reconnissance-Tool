<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VAJRA Security Report - example.com</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #2c3e50;
            --secondary: #3498db;
            --accent: #e74c3c;
            --success: #27ae60;
            --warning: #f39c12;
            --danger: #c0392b;
            --light: #ecf0f1;
            --dark: #2c3e50;
            --gradient-start: #667eea;
            --gradient-end: #764ba2;
            --executive-bg: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            --domain-bg: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            --subdomain-bg: linear-gradient(135deg, #cce5ff 0%, #b8daff 100%);
            --service-bg: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            --network-bg: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            --security-bg: linear-gradient(135deg, #d6d8d9 0%, #c6c8ca 100%);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
            color: #333;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                url('https://images.unsplash.com/photo-1544890225-2f3faec4cd60?w=500&h=500&fit=crop') center/cover,
                url('https://images.unsplash.com/photo-1563207153-f403bf289096?w=500&h=500&fit=crop') 20% 30%/cover,
                url('https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=500&h=500&fit=crop') 80% 70%/cover;
            background-blend-mode: overlay;
            opacity: 0.05;
            pointer-events: none;
            z-index: -1;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header Styles */
        .header {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(245, 245, 245, 0.98) 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            border: 2px solid var(--secondary);
        }
        
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .vajra-title {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24, #f39c12, #27ae60, #3498db, #9b59b6, #ff6b6b);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5em;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            animation: rainbow 8s ease-in-out infinite;
        }
        
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .vajra-subtitle {
            color: var(--primary);
            font-size: 1.2em;
            font-weight: 600;
            letter-spacing: 1px;
            margin: 5px 0 20px 0;
        }
        
        .report-title {
            color: var(--secondary);
            font-size: 2.2em;
            margin: 20px 0 15px 0;
            padding-top: 20px;
            border-top: 3px solid var(--accent);
            font-weight: 700;
        }
        
        .download-btn {
            background: linear-gradient(45deg, var(--accent), var(--danger));
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(231, 76, 60, 0.6);
        }
        
        /* Scan Info */
        .scan-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .info-item {
            background: linear-gradient(135deg, var(--secondary) 0%, #2980b9 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .info-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
        }
        
        .info-item h3 {
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        .info-item p {
            font-size: 1em;
            font-weight: 600;
        }
        
        .copy-badge {
            position: absolute;
            top: 5px;
            right: 5px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8em;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .info-item:hover .copy-badge {
            opacity: 1;
        }
        
        /* Section Styles */
        .section {
            background: rgba(255, 255, 255, 0.97);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
            margin-bottom: 25px;
            border-left: 5px solid var(--secondary);
        }
        
        .section.executive { background: var(--executive-bg); border-left-color: #ffc107; }
        .section.domain { background: var(--domain-bg); border-left-color: #28a745; }
        .section.subdomain { background: var(--subdomain-bg); border-left-color: #007bff; }
        .section.service { background: var(--service-bg); border-left-color: #17a2b8; }
        .section.network { background: var(--network-bg); border-left-color: #dc3545; }
        .section.security { background: var(--security-bg); border-left-color: #6c757d; }
        
        .section h2 {
            color: var(--primary);
            border-bottom: 2px solid var(--accent);
            padding-bottom: 12px;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Compact Tables */
        .compact-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .compact-table th {
            background: linear-gradient(135deg, var(--secondary) 0%, #2980b9 100%);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        
        .compact-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #dee2e6;
        }
        
        .compact-table tr:last-child td {
            border-bottom: none;
        }
        
        .compact-table tr:hover {
            background: #f8f9fa;
        }
        
        .status-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .status-200 { background: #d4edda; color: #155724; }
        .status-302 { background: #fff3cd; color: #856404; }
        .status-404 { background: #f8d7da; color: #721c24; }
        
        /* Service Grid */
        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .service-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--secondary);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        
        .service-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .service-port {
            font-weight: 700;
            color: var(--primary);
        }
        
        .service-details {
            font-size: 0.9em;
            color: #6c757d;
            line-height: 1.5;
        }
        
        .service-recommendation {
            margin-top: 8px;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
            border-left: 3px solid var(--warning);
            font-size: 0.85em;
        }
        
        /* Code Copy Blocks */
        .code-block {
            position: relative;
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }
        
        .copy-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8em;
            transition: background 0.3s ease;
        }
        
        .copy-button:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 40px;
            color: white;
            padding: 25px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
        }
        
        .footer p {
            margin: 8px 0;
        }
        
        .contact-info {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 15px;
        }
        
        .contact-link {
            color: #fff;
            text-decoration: none;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9em;
        }
        
        .contact-link:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        /* Responsive Design */
        @media (max-width: 1024px) {
            .container {
                padding: 15px;
            }
            
            .header {
                padding: 25px 15px;
            }
            
            .vajra-title {
                font-size: 2.8em;
            }
            
            .header-top {
                flex-direction: column;
                gap: 15px;
            }
        }
        
        @media (max-width: 768px) {
            .scan-info {
                grid-template-columns: 1fr;
            }
            
            .vajra-title {
                font-size: 2.2em;
            }
            
            .vajra-subtitle {
                font-size: 1em;
            }
            
            .section {
                padding: 20px 15px;
            }
            
            .service-grid {
                grid-template-columns: 1fr;
            }
            
            .contact-info {
                flex-direction: column;
                align-items: center;
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .section {
            animation: fadeIn 0.6s ease-out;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <div class="header">
            <div class="header-top">
                <div>
                    <div class="vajra-title">VAJRA</div>
                    <div class="vajra-subtitle">Multi-layered Red Team Reconnaissance Framework</div>
                </div>
                <a href="report_example.com.pdf" class="download-btn" download>
                    <i class="fas fa-file-pdf"></i> Download PDF
                </a>
            </div>
            
            <div class="report-title">Comprehensive Security Assessment Report</div>
            
            <div class="scan-info">
                <div class="info-item" onclick="copyToClipboard('example.com')">
                    <span class="copy-badge"><i class="fas fa-copy"></i></span>
                    <h3><i class="fas fa-bullseye"></i> Target</h3>
                    <p>example.com</p>
                </div>
                <div class="info-item">
                    <h3><i class="fas fa-calendar-alt"></i> Scan Date</h3>
                    <p id="currentDate">August 31, 2025</p>
                </div>
                <div class="info-item">
                    <h3><i class="fas fa-check-circle"></i> Status</h3>
                    <p>Completed</p>
                </div>
                <div class="info-item">
                    <h3><i class="fas fa-shield-alt"></i> Risk Level</h3>
                    <p>Medium</p>
                </div>
            </div>
        </div>

        <!-- Executive Summary -->
        <div class="section executive">
            <h2><i class="fas fa-chart-line"></i> Executive Summary</h2>
            <div class="code-block">
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
                <code>Overall Assessment: Target demonstrates moderate security posture with areas requiring immediate attention.</code>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 15px 0;">
                <div style="background: var(--success); color: white; padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5em; font-weight: bold;">3</div>
                    <div>Low Risk</div>
                </div>
                <div style="background: var(--warning); color: white; padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5em; font-weight: bold;">2</div>
                    <div>Medium Risk</div>
                </div>
                <div style="background: var(--accent); color: white; padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5em; font-weight: bold;">1</div>
                    <div>High Risk</div>
                </div>
                <div style="background: var(--danger); color: white; padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 1.5em; font-weight: bold;">0</div>
                    <div>Critical Risk</div>
                </div>
            </div>
        </div>

        <!-- Domain Information Section -->
        <div class="section domain">
            <h2><i class="fas fa-globe"></i> Domain Registration Analysis</h2>
            <div class="code-block">
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
                <code>Domain: example.com | Registrar: Example Registrar Inc. | Created: 1995-08-15 | Expires: 2025-08-14</code>
            </div>
            
            <table class="compact-table">
                <tr>
                    <td><strong>Name Servers</strong></td>
                    <td>ns1.example.com, ns2.example.com</td>
                </tr>
                <tr>
                    <td><strong>DNSSEC</strong></td>
                    <td><span style="color: var(--success);">Enabled</span></td>
                </tr>
                <tr>
                    <td><strong>Registration Period</strong></td>
                    <td>30 years (Established 1995)</td>
                </tr>
            </table>
        </div>

        <!-- Subdomains Section -->
        <div class="section subdomain">
            <h2><i class="fas fa-sitemap"></i> Subdomain Infrastructure Mapping</h2>
            <div class="code-block">
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
                <code>Discovered 15 subdomains | Tools: Subfinder + Amass | Coverage: 98%</code>
            </div>
            
            <table class="compact-table">
                <thead>
                    <tr>
                        <th>Subdomain</th>
                        <th>Type</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>api.example.com</td><td>API Endpoint</td><td><span class="status-badge status-200">Active</span></td></tr>
                    <tr><td>admin.example.com</td><td>Admin Panel</td><td><span class="status-badge status-302">Redirect</span></td></tr>
                    <tr><td>mail.example.com</td><td>Email Service</td><td><span class="status-badge status-200">Active</span></td></tr>
                    <tr><td>test.example.com</td><td>Testing</td><td><span class="status-badge status-404">Inactive</span></td></tr>
                    <tr><td>dev.example.com</td><td>Development</td><td><span class="status-badge status-200">Active</span></td></tr>
                </tbody>
            </table>
        </div>

        <!-- Service Discovery Section -->
        <div class="section service">
            <h2><i class="fas fa-heartbeat"></i> Service Discovery & Availability</h2>
            <div class="code-block">
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
                <code>Active Services: 8/15 | Tool: HTTPX | Avg Response: 187ms</code>
            </div>
            
            <table class="compact-table">
                <thead>
                    <tr>
                        <th>Service URL</th>
                        <th>Status</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>https://example.com</td><td><span class="status-badge status-200">200 OK</span></td><td>Main Application</td></tr>
                    <tr><td>https://api.example.com</td><td><span class="status-badge status-200">200 OK</span></td><td>REST API</td></tr>
                    <tr><td>http://admin.example.com</td><td><span class="status-badge status-302">302 Redirect</span></td><td>Admin Panel</td></tr>
                    <tr><td>https://mail.example.com</td><td><span class="status-badge status-200">200 OK</span></td><td>Webmail</td></tr>
                </tbody>
            </table>
        </div>

        <!-- Network Analysis Section -->
        <div class="section network">
            <h2><i class="fas fa-network-wired"></i> Network Infrastructure Analysis</h2>
            <div class="code-block">
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
                <code>Open Ports: 3 | Scan Type: TCP SYN | Duration: 2m 45s</code>
            </div>
            
            <div class="service-grid">
                <div class="service-item">
                    <div class="service-header">
                        <span class="service-port">Port 80/tcp</span>
                        <span style="color: var(--high); font-weight: 600;">HTTP</span>
                    </div>
                    <div class="service-details">
                        Apache/2.4.52 (Ubuntu) | Web traffic, unencrypted
                    </div>
                    <div class="service-recommendation">
                        <i class="fas fa-exclamation-triangle"></i> Recommendation: Redirect to HTTPS
                    </div>
                </div>
                
                <div class="service-item">
                    <div class="service-header">
                        <span class="service-port">Port 443/tcp</span>
                        <span style="color: var(--medium); font-weight: 600;">HTTPS</span>
                    </div>
                    <div class="service-details">
                        Apache/2.4.52 (Ubuntu) | TLS 1.3 Supported
                    </div>
                </div>
                
                <div class="service-item">
                    <div class="service-header">
                        <span class="service-port">Port 22/tcp</span>
                        <span style="color: var(--medium); font-weight: 600;">SSH</span>
                    </div>
                    <div class="service-details">
                        OpenSSH 8.9p1 Ubuntu 3 | Curve25519 Key Exchange
                    </div>
                </div>
            </div>
        </div>

        <!-- Security Recommendations -->
        <div class="section security">
            <h2><i class="fas fa-clipboard-check"></i> Security Recommendations</h2>
            <div class="code-block">
                <button class="copy-button" onclick="copyCode(this)">Copy</button>
                <code>Priority Actions: HTTPS redirect, TLS hardening, Security headers, WAF implementation</code>
            </div>
            
            <table class="compact-table">
                <thead>
                    <tr>
                        <th>Priority</th>
                        <th>Recommendation</th>
                        <th>Timeline</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td><span style="color: var(--high);">High</span></td><td>Implement HTTP to HTTPS redirect</td><td>Immediate</td></tr>
                    <tr><td><span style="color: var(--high);">High</span></td><td>Disable deprecated TLS versions</td><td>Immediate</td></tr>
                    <tr><td><span style="color: var(--medium);">Medium</span></td><td>Configure security headers (HSTS, CSP)</td><td>1 Week</td></tr>
                    <tr><td><span style="color: var(--medium);">Medium</span></td><td>Implement WAF protection</td><td>2 Weeks</td></tr>
                </tbody>
            </table>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>Generated by VAJRA Framework - Multi-layered Red Team Reconnaissance Framework</strong></p>
            <p>Owner: Yash Javiya | Penetration Tester</p>
            
            <div class="contact-info">
                <a href="https://www.linkedin.com/in/yash--javiya/" class="contact-link" target="_blank">
                    <i class="fab fa-linkedin"></i> LinkedIn
                </a>
                <a href="mailto:yashjaviya1111@gmail.com" class="contact-link">
                    <i class="fas fa-envelope"></i> Email
                </a>
                <a href="https://github.com/yashjaviya111" class="contact-link" target="_blank">
                    <i class="fab fa-github"></i> GitHub
                </a>
                <a href="tel:+919999999999" class="contact-link">
                    <i class="fas fa-phone"></i> Contact
                </a>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Set current date
            const now = new Date();
            const options = { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            const dateString = now.toLocaleDateString('en-US', options);
            
            document.getElementById('currentDate').textContent = dateString;
            
            console.log('VAJRA Professional Security Report loaded successfully');
        });

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied to clipboard: ' + text);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        }

        function copyCode(button) {
            const codeBlock = button.parentElement;
            const code = codeBlock.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = originalText;
                }, 2000);
            });
        }
    </script>
</body>
</html>
