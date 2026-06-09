"use client";

import { useState, useEffect } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { 
  Search, 
  Plus, 
  Cpu, 
  Code2, 
  Database, 
  Layout, 
  Terminal, 
  Wrench,
  TrendingUp,
  ShieldCheck,
  Loader2
} from "lucide-react";
import api from "@/lib/axios";

interface Skill {
  id: string;
  name: string;
  category: string;
  level: "beginner" | "intermediate" | "advanced" | "expert";
  market_demand: number; // 0 to 100
  is_normalized: boolean;
}

const CATEGORIES = [
  { id: "all", label: "Tous", icon: <Layout size={18} /> },
  { id: "frontend", label: "Frontend", icon: <Layout size={18} /> },
  { id: "backend", label: "Backend", icon: <Database size={18} /> },
  { id: "ai", label: "IA & Data", icon: <Cpu size={18} /> },
  { id: "devops", label: "DevOps", icon: <Terminal size={18} /> },
  { id: "tools", label: "Outils", icon: <Wrench size={18} /> },
];

export default function SkillsPage() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [activeCategory, setActiveCategory] = useState("all");

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await api.get("/skills/");
        setSkills(response.data);
      } catch (error) {
        console.error("Failed to fetch skills:", error);
        setSkills([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSkills();
  }, []);

  const filteredSkills = skills.filter(skill => {
    const matchesSearch = skill.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = activeCategory === "all" || skill.category === activeCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <DashboardLayout>
      <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Compétences & Taxonomie</h2>
            <p className="text-muted-foreground mt-1">
              Gérez vos compétences extraites et visualisez leur pertinence sur le marché actuel.
            </p>
          </div>
          <button className="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2.5 rounded-lg text-sm font-semibold hover:bg-primary/90 transition-all shadow-md">
            <Plus size={18} />
            Ajouter une compétence
          </button>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <input
              type="text"
              placeholder="Rechercher une compétence (ex: JavaScript, AWS...)"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-card border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 no-scrollbar">
            {CATEGORIES.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
                  activeCategory === cat.id
                    ? "bg-primary text-primary-foreground shadow-md"
                    : "bg-card border text-muted-foreground hover:bg-accent"
                }`}
              >
                {cat.icon}
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Skills Grid */}
        {loading ? (
          <div className="flex h-64 items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary opacity-50" />
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {filteredSkills.map((skill) => (
              <SkillCard key={skill.id} skill={skill} />
            ))}
            {filteredSkills.length === 0 && (
              <div className="col-span-full py-12 text-center border-2 border-dashed rounded-2xl bg-muted/5">
                <p className="text-muted-foreground">Aucune compétence trouvée dans cette catégorie.</p>
              </div>
            )}
          </div>
        )}

        {/* AI Insight Section */}
        <div className="rounded-2xl border bg-gradient-to-br from-primary/5 via-background to-blue-500/5 p-8 border-primary/10">
          <div className="flex flex-col md:flex-row items-start gap-6">
            <div className="p-4 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <ShieldCheck size={32} />
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-bold">Normalisation IA Active</h3>
              <p className="text-muted-foreground text-sm leading-relaxed max-w-3xl">
                Notre <strong>SkillExtractionAgent</strong> utilise une taxonomie centralisée pour garantir que vos compétences sont toujours comparables aux offres du marché. 
                Que vous écriviez "JS", "ES6" ou "Javascript", l'IA les regroupe automatiquement sous l'entité canonique <strong>JavaScript</strong>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function SkillCard({ skill }: { skill: Skill }) {
  const getLevelColor = (level: string) => {
    switch (level) {
      case "expert": return "text-purple-500 bg-purple-500/10 border-purple-500/20";
      case "advanced": return "text-blue-500 bg-blue-500/10 border-blue-500/20";
      case "intermediate": return "text-emerald-500 bg-emerald-500/10 border-emerald-500/20";
      default: return "text-slate-500 bg-slate-500/10 border-slate-500/20";
    }
  };

  return (
    <div className="group rounded-xl border bg-card p-5 shadow-sm hover-lift transition-all duration-300 relative overflow-hidden">
      <div className="flex justify-between items-start mb-4">
        <h4 className="font-bold text-lg group-hover:text-primary transition-colors">{skill.name}</h4>
        <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${getLevelColor(skill.level)}`}>
          {skill.level}
        </span>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground flex items-center gap-1">
            <TrendingUp size={12} /> Demande Marché
          </span>
          <span className="font-bold text-foreground">{skill.market_demand}%</span>
        </div>
        <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
          <div 
            className="h-full bg-primary transition-all duration-1000 ease-out"
            style={{ width: `${skill.market_demand}%` }}
          />
        </div>
      </div>

      {/* Background Decor */}
      <div className="absolute -bottom-2 -right-2 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity">
        <Code2 size={80} />
      </div>
    </div>
  );
}
