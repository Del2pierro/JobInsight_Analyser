"use client";

import { useState, useEffect } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { TrendsChart } from "@/components/dashboard/TrendsChart";
import { 
  Users, 
  Briefcase, 
  TrendingUp, 
  Clock, 
  ArrowUpRight, 
  Search,
  CheckCircle2,
  Loader2
} from "lucide-react";
import api from "@/lib/axios";

export default function DashboardPage() {
  const [stats, setStats] = useState<any[]>([]);
  const [recentJobs, setRecentJobs] = useState<any[]>([]);
  const [trendsData, setTrendsData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsRes, jobsRes, trendsRes] = await Promise.all([
          api.get("/trends/stats"),
          api.get("/jobs/?limit=4"),
          api.get("/trends/top-skills")
        ]);
        
        setStats(statsRes.data);
        setRecentJobs(jobsRes.data);
        setTrendsData(trendsRes.data);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex h-[70vh] items-center justify-center">
          <Loader2 className="h-12 w-12 animate-spin text-primary opacity-50" />
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header Section */}
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Tableau de bord</h2>
          <p className="text-muted-foreground">
            Bienvenue. Voici un aperçu des tendances actuelles du marché de l'emploi tech.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, index) => (
            <div key={index} className="rounded-xl border bg-card p-6 shadow-sm">
              <div className="flex items-center justify-between space-y-0 pb-2">
                <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                <div className="p-2 bg-muted rounded-lg">{stat.icon}</div>
              </div>
              <div className="flex items-baseline space-x-2">
                <h3 className="text-2xl font-bold">{stat.value}</h3>
                <span className="text-xs font-medium text-green-500 flex items-center">
                  <ArrowUpRight size={12} className="mr-0.5" />
                  {stat.change}
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-1">{stat.description}</p>
            </div>
          ))}
        </div>

        {/* Charts and Recent Content */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
          {/* Main Chart */}
          <div className="col-span-4 rounded-xl border bg-card p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold">Compétences les plus demandées</h3>
                <p className="text-sm text-muted-foreground">Volume d'offres par technologie</p>
              </div>
            </div>
            <TrendsChart data={trendsData} />
          </div>

          {/* Recent Jobs */}
          <div className="col-span-3 rounded-xl border bg-card p-6 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">Offres récentes</h3>
              <button className="text-sm text-primary hover:underline font-medium">Voir tout</button>
            </div>
            <div className="space-y-6">
              {recentJobs.map((job) => (
                <div key={job.id} className="flex items-start justify-between border-b border-border/50 pb-4 last:border-0 last:pb-0">
                  <div className="space-y-1">
                    <p className="text-sm font-semibold leading-none hover:text-primary cursor-pointer transition-colors">
                      {job.title}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {job.company} • {job.location}
                    </p>
                    <div className="flex items-center pt-1 text-[10px] text-muted-foreground">
                      <Clock size={10} className="mr-1" />
                      {job.date}
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <div className={`text-xs font-bold px-2 py-1 rounded-full ${
                      job.match > 80 ? "bg-green-500/10 text-green-500" : "bg-amber-500/10 text-amber-500"
                    }`}>
                      {job.match}% match
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions / Integration Info */}
        <div className="rounded-xl border bg-gradient-to-r from-blue-600/10 to-purple-600/10 p-8 border-primary/20">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center md:text-left">
              <h3 className="text-xl font-bold">Lancez une nouvelle analyse de marché</h3>
              <p className="text-muted-foreground max-w-md">
                Notre agent de collecte parcourt le web pour vous apporter les dernières données tech en temps réel.
              </p>
            </div>
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-bold shadow-lg shadow-primary/20 hover:scale-105 transition-transform">
                Lancer le Scraping
              </button>
              <button className="px-6 py-3 bg-card border rounded-lg font-bold hover:bg-accent transition-colors">
                Importer un CV
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
