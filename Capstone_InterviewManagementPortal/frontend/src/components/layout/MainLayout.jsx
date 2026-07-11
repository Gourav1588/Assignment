import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { NAV_ITEMS, ROUTES } from '../../constants/route'
import './MainLayout.css'

export default function MainLayout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  const navItems = NAV_ITEMS[user?.role] || []

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-brand">Interview Portal</div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? 'nav-link--active' : ''}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user-name">{user?.full_name}</div>
          <div className="sidebar-user-role">{user?.role}</div>
          <Link
            to={ROUTES.CHANGE_PASSWORD}
            className="nav-link"
            style={{ fontSize: '12px', marginBottom: '8px', padding: '6px 8px' }}>

            Change Password
          </Link>

          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </aside>

      <div className="main-content">
        <header className="top-header">
          <span>{user?.email}</span>
        </header>
        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  )
}