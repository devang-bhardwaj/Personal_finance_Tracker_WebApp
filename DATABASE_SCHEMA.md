# Database Schema Analysis & Enterprise Design

## 📊 **Current Database Schema Analysis**

### **Inferred Current Schema** (Based on Code Analysis)

```sql
-- Current tables inferred from codebase:

-- Users table (implied but not implemented properly)
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table (from transaction-related code)
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    transaction_type ENUM('Income', 'Expense', 'Transfer') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Budget table (from budget.py)
CREATE TABLE Budget (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
```

### **Current Schema Issues**

#### 🚨 **Critical Issues**
1. **No proper foreign key relationships**
2. **Missing essential tables** (Categories, Accounts, etc.)
3. **No data integrity constraints**
4. **Limited transaction types**
5. **No audit trail or versioning**
6. **No multi-tenancy support**
7. **Missing indexes for performance**

#### 🔍 **Data Quality Issues**
1. **No data validation at database level**
2. **No enum constraints for consistent data**
3. **Missing required fields**
4. **No soft delete mechanism**
5. **No data archiving strategy**

---

## 🎯 **Enterprise-Level Database Schema Design**

### **Core Entity Relationship Diagram**

```
Organizations (Multi-tenancy)
    ↓
Users (Authentication & Profiles)
    ↓
Accounts (Bank, Credit Card, Cash, Investment)
    ↓
Categories (Income/Expense Classification)
    ↓
Transactions (Financial Activities)
    ↓
Budgets (Financial Planning)
    ↓
Goals (Financial Objectives)
    ↓
Reports (Analytics & Insights)
```

---

## 📋 **Complete Enterprise Database Schema**

### **1. Organizations & Multi-Tenancy**

```sql
-- Organizations table for multi-tenancy
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    subscription_tier VARCHAR(50) DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Organization members/users relationship
CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    permissions JSONB DEFAULT '{}',
    invited_by UUID,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, user_id)
);
```

### **2. Enhanced User Management**

```sql
-- Users table with comprehensive profile
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    timezone VARCHAR(50) DEFAULT 'UTC',
    language VARCHAR(10) DEFAULT 'en',
    currency VARCHAR(10) DEFAULT 'USD',
    is_email_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User sessions for security tracking
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Password reset tokens
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### **3. Financial Accounts System**

```sql
-- Account types and categories
CREATE TABLE account_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'asset', 'liability', 'equity'
    description TEXT,
    is_active BOOLEAN DEFAULT true
);

-- Financial accounts
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    account_type_id UUID NOT NULL REFERENCES account_types(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    account_number VARCHAR(100),
    bank_name VARCHAR(255),
    currency VARCHAR(10) DEFAULT 'USD',
    initial_balance DECIMAL(15,2) DEFAULT 0.00,
    current_balance DECIMAL(15,2) DEFAULT 0.00,
    credit_limit DECIMAL(15,2),
    interest_rate DECIMAL(5,4),
    is_active BOOLEAN DEFAULT true,
    is_default BOOLEAN DEFAULT false,
    external_id VARCHAR(255), -- For bank API integration
    last_synced_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Account balance history for tracking
CREATE TABLE account_balance_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    balance DECIMAL(15,2) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### **4. Advanced Transaction System**

```sql
-- Transaction categories with hierarchy
CREATE TABLE transaction_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES transaction_categories(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_type VARCHAR(50) NOT NULL, -- 'income', 'expense', 'transfer'
    color VARCHAR(7), -- Hex color code
    icon VARCHAR(50),
    is_system BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Transaction tags for flexible labeling
CREATE TABLE transaction_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(7),
    UNIQUE(user_id, name)
);

-- Enhanced transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    category_id UUID REFERENCES transaction_categories(id),
    transfer_account_id UUID REFERENCES accounts(id), -- For transfers
    
    -- Transaction details
    transaction_type VARCHAR(50) NOT NULL, -- 'income', 'expense', 'transfer'
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    exchange_rate DECIMAL(10,6) DEFAULT 1.0,
    
    -- Description and metadata
    description TEXT NOT NULL,
    notes TEXT,
    reference_number VARCHAR(255),
    external_id VARCHAR(255), -- Bank transaction ID
    
    -- Dates
    transaction_date DATE NOT NULL,
    posted_date DATE,
    
    -- Status and workflow
    status VARCHAR(50) DEFAULT 'completed', -- 'pending', 'completed', 'cancelled'
    is_recurring BOOLEAN DEFAULT false,
    recurring_rule_id UUID,
    
    -- Location data
    location_name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Attachments
    receipt_url VARCHAR(500),
    attachment_urls JSONB,
    
    -- Audit fields
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT positive_amount CHECK (amount > 0),
    CONSTRAINT valid_transfer CHECK (
        (transaction_type != 'transfer') OR (transfer_account_id IS NOT NULL)
    )
);

-- Transaction tags relationship
CREATE TABLE transaction_tag_assignments (
    transaction_id UUID NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES transaction_tags(id) ON DELETE CASCADE,
    PRIMARY KEY (transaction_id, tag_id)
);

-- Recurring transaction rules
CREATE TABLE recurring_transaction_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    template_data JSONB NOT NULL,
    frequency VARCHAR(50) NOT NULL, -- 'daily', 'weekly', 'monthly', 'yearly'
    interval_value INTEGER DEFAULT 1,
    start_date DATE NOT NULL,
    end_date DATE,
    next_execution_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### **5. Budget Management System**

```sql
-- Budget templates
CREATE TABLE budget_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    template_data JSONB NOT NULL,
    is_public BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Budget periods and plans
CREATE TABLE budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    period_type VARCHAR(50) NOT NULL, -- 'monthly', 'quarterly', 'yearly', 'custom'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_budget DECIMAL(15,2),
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed', 'cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Budget line items
CREATE TABLE budget_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    budget_id UUID NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
    category_id UUID REFERENCES transaction_categories(id),
    name VARCHAR(255) NOT NULL,
    budgeted_amount DECIMAL(15,2) NOT NULL,
    spent_amount DECIMAL(15,2) DEFAULT 0.00,
    rollover_from_previous DECIMAL(15,2) DEFAULT 0.00,
    notes TEXT,
    CONSTRAINT positive_budget CHECK (budgeted_amount >= 0)
);

-- Budget alerts and notifications
CREATE TABLE budget_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    budget_item_id UUID NOT NULL REFERENCES budget_items(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- 'threshold', 'exceeded', 'warning'
    threshold_percentage INTEGER NOT NULL,
    is_enabled BOOLEAN DEFAULT true,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### **6. Financial Goals & Planning**

```sql
-- Financial goals
CREATE TABLE financial_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    goal_type VARCHAR(50) NOT NULL, -- 'savings', 'debt_reduction', 'investment'
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) DEFAULT 0.00,
    target_date DATE,
    monthly_contribution DECIMAL(15,2),
    category_id UUID REFERENCES transaction_categories(id),
    account_id UUID REFERENCES accounts(id),
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed', 'paused', 'cancelled'
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Goal progress tracking
CREATE TABLE goal_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    goal_id UUID NOT NULL REFERENCES financial_goals(id) ON DELETE CASCADE,
    amount DECIMAL(15,2) NOT NULL,
    transaction_id UUID REFERENCES transactions(id),
    notes TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### **7. Reporting & Analytics**

```sql
-- Custom reports
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    report_type VARCHAR(50) NOT NULL,
    configuration JSONB NOT NULL,
    is_scheduled BOOLEAN DEFAULT false,
    schedule_expression VARCHAR(100), -- Cron expression
    is_shared BOOLEAN DEFAULT false,
    last_generated_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Report executions history
CREATE TABLE report_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    execution_time_ms INTEGER,
    row_count INTEGER,
    file_url VARCHAR(500),
    status VARCHAR(50) NOT NULL, -- 'success', 'failed', 'running'
    error_message TEXT,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### **8. Audit & Security**

```sql
-- Audit log for all changes
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'create', 'update', 'delete'
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- API access logs
CREATE TABLE api_access_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    method VARCHAR(10) NOT NULL,
    endpoint VARCHAR(500) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    ip_address INET,
    user_agent TEXT,
    request_body JSONB,
    response_body JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 **Database Indexes & Performance**

### **Critical Indexes**

```sql
-- User authentication indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_user_sessions_token ON user_sessions(token_hash);

-- Transaction performance indexes
CREATE INDEX idx_transactions_user_date ON transactions(user_id, transaction_date DESC);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_category ON transactions(category_id);
CREATE INDEX idx_transactions_type_date ON transactions(transaction_type, transaction_date);

-- Account indexes
CREATE INDEX idx_accounts_user ON accounts(user_id);
CREATE INDEX idx_accounts_type ON accounts(account_type_id);

-- Budget indexes
CREATE INDEX idx_budgets_user_period ON budgets(user_id, start_date, end_date);
CREATE INDEX idx_budget_items_budget ON budget_items(budget_id);

-- Audit and security indexes
CREATE INDEX idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_logs_user_date ON audit_logs(user_id, created_at DESC);
```

### **Composite Indexes for Complex Queries**

```sql
-- For financial reporting
CREATE INDEX idx_transactions_user_category_date ON transactions(user_id, category_id, transaction_date);
CREATE INDEX idx_transactions_account_type_date ON transactions(account_id, transaction_type, transaction_date);

-- For budget analysis
CREATE INDEX idx_budget_items_category_period ON budget_items(category_id, budget_id);

-- For goal tracking
CREATE INDEX idx_goal_progress_goal_date ON goal_progress(goal_id, recorded_at DESC);
```

---

## 🔄 **Database Migration Strategy**

### **Phase 1: Data Migration (Week 1)**
1. **Export existing data** from current MySQL tables
2. **Create new PostgreSQL schema**
3. **Data cleaning and validation**
4. **Import with proper UUID generation**

### **Phase 2: Application Updates (Week 2)**
1. **Update SQLAlchemy models**
2. **Create Alembic migration scripts**
3. **Update all database queries**
4. **Test data integrity**

### **Phase 3: Performance Optimization (Week 3)**
1. **Add all indexes**
2. **Optimize query performance**
3. **Add database constraints**
4. **Performance testing**

---

## 📊 **Data Validation & Constraints**

### **Business Rules Implementation**

```sql
-- Ensure account balances are consistent
CREATE OR REPLACE FUNCTION validate_account_balance()
RETURNS TRIGGER AS $$
BEGIN
    -- Update account balance after transaction
    UPDATE accounts 
    SET current_balance = (
        SELECT COALESCE(SUM(
            CASE 
                WHEN t.transaction_type = 'income' THEN t.amount
                WHEN t.transaction_type = 'expense' THEN -t.amount
                WHEN t.transaction_type = 'transfer' AND t.account_id = NEW.account_id THEN -t.amount
                WHEN t.transaction_type = 'transfer' AND t.transfer_account_id = NEW.account_id THEN t.amount
                ELSE 0
            END
        ), 0) + initial_balance
        FROM transactions t 
        WHERE t.account_id = NEW.account_id OR t.transfer_account_id = NEW.account_id
    )
    WHERE id = NEW.account_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_account_balance
    AFTER INSERT OR UPDATE OR DELETE ON transactions
    FOR EACH ROW EXECUTE FUNCTION validate_account_balance();
```

This comprehensive database schema provides the foundation for an enterprise-level personal finance application with proper data integrity, security, and scalability considerations.