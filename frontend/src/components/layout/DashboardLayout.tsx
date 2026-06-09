import { ReactNode } from "react";
import Link from "next/link";
import { LayoutDashboard, Briefcase, FileText, TrendingUp, Settings, LogOut } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const { user, logout } = useAuth();

  const getInitials = (name: string) => {
    if (!name) return "??";
    return name.split(" ").map(n => n[0]).join("").toUpperCase();
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar latérale */}
      <aside className="w-64 border-r bg-card hidden md:flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-400">
            JobInsight AI
          </h1>
        </div>
        <nav className="flex-1 overflow-y-auto p-4 space-y-2">
          <NavItem href="/" icon={<LayoutDashboard size={20} />} label="Tableau de bord" active />
          <NavItem href="/jobs" icon={<Briefcase size={20} />} label="Offres d'emploi" />
          <NavItem href="/resumes" icon={<FileText size={20} />} label="Mes CVs" />
          <NavItem href="/trends" icon={<TrendingUp size={20} />} label="Tendances" />
        </nav>
        <div className="p-4 border-t">
          <NavItem href="/settings" icon={<Settings size={20} />} label="Paramètres" />
          <button 
            onClick={logout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 transition-colors mt-2"
          >
            <LogOut size={20} />
            Déconnexion
          </button>
        </div>
      </aside>

      {/* Contenu principal */}
      <main className="flex-1 overflow-y-auto">
        <header className="h-16 border-b bg-background/80 backdrop-blur-md sticky top-0 z-10 flex items-center px-6 justify-end shadow-sm">
          <div className="flex items-center gap-4">
            <span className="text-sm font-medium text-muted-foreground mr-2">
              {user?.full_name || "Utilisateur"}
            </span>
            <div className="w-9 h-9 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold border border-primary/30 shadow-inner">
              {user?.full_name ? getInitials(user.full_name) : "PR"}
            </div>
          </div>
        </header>
        <div className="p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}


function NavItem({ href, icon, label, active = false }: { href: string, icon: ReactNode, label: string, active?: boolean }) {
  return (
    <Link 
      href={href} 
      className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
        active 
          ? "bg-primary text-primary-foreground shadow-md" 
          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
      }`}
    >
      {icon}
      {label}
    </Link>
  );
}
