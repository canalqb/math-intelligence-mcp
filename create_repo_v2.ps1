$params = @{name='math-intelligence-mcp'; description='Math Intelligence MCP - Mathematical Intelligence for AI Agents'; private=$false; initialize_with_readme=$true}
$headers = @{'Accept'='application/vnd.github+json'}
$response = Invoke-RestMethod -Method Post -Uri 'https://api.github.com/user/repos' -Headers $headers -Body $params
Write-Host "Repositório criado: $($response.html_url)"
Write-Host "Full name: $($response.full_name)"
Write-Host "Private: $($response.private)"