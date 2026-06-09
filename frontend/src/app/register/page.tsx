"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/axios";
import { Activity } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export default function RegisterPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // 1. Création du compte via l'API FastAPI (schema: UserCreate)
      await api.post("/auth/register", {
        email,
        password,
        full_name: fullName,
        role: "candidate",
      });

      // 2. Connexion automatique juste après l'inscription
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const loginResponse = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      if (loginResponse.data && loginResponse.data.access_token) {
        await login(loginResponse.data.access_token, loginResponse.data.refresh_token);
      }
    } catch (err: any) {
      setError(err.response?.data?.message || "Une erreur est survenue lors de l'inscription.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-row-reverse">
      {/* Côté droit : Branding (inversé par rapport au login pour la dynamique) */}
      <div className="hidden lg:flex w-1/2 bg-slate-900 relative flex-col justify-center items-center overflow-hidden border-l border-border/50">
        <div className="absolute inset-0 bg-gradient-to-bl from-primary/20 via-background to-background" />
        <div className="relative z-10 text-center px-12 animate-in fade-in slide-in-from-top-8 duration-1000">
          <div className="w-20 h-20 mx-auto bg-primary/20 rounded-2xl flex items-center justify-center mb-8 border border-primary/30 shadow-xl">
             <Activity className="h-10 w-10 text-primary animate-pulse" />
          </div>
          <h2 className="text-3xl font-bold mb-4 text-white drop-shadow-md">Prenez le contrôle</h2>
          <p className="text-lg text-slate-300 max-w-md mx-auto leading-relaxed">
            Découvrez en un instant les compétences qu'il vous manque pour décrocher le job de vos rêves.
          </p>
        </div>
      </div>

      {/* Côté gauche : Formulaire d'inscription */}
      <div className="flex-1 flex flex-col justify-center px-4 sm:px-6 lg:flex-none lg:w-1/2 bg-background">
        <div className="mx-auto w-full max-w-sm lg:w-[400px] animate-in fade-in duration-700">
          <div>
            <h2 className="mt-6 text-3xl font-bold tracking-tight text-foreground">
              Créez votre compte
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Rejoignez JobInsight AI et boostez votre carrière.
            </p>
          </div>

          <div className="mt-8">
            <form onSubmit={handleRegister} className="space-y-5">
              {error && (
                <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm p-3 rounded-md animate-in slide-in-from-top-2">
                  {error}
                </div>
              )}
              
              <div>
                <label className="block text-sm font-medium text-foreground">Nom complet</label>
                <div className="mt-1.5">
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="block w-full rounded-md border border-input bg-background/50 py-2.5 px-3 text-foreground shadow-sm transition-colors focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    placeholder="Pierre Dupont"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground">Adresse Email</label>
                <div className="mt-1.5">
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full rounded-md border border-input bg-background/50 py-2.5 px-3 text-foreground shadow-sm transition-colors focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    placeholder="pierre@exemple.com"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground">Mot de passe</label>
                <div className="mt-1.5">
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="block w-full rounded-md border border-input bg-background/50 py-2.5 px-3 text-foreground shadow-sm transition-colors focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:text-sm"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="flex w-full justify-center rounded-md bg-primary py-2.5 px-3 text-sm font-semibold text-primary-foreground shadow-md hover:bg-primary/90 hover:shadow-lg focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:opacity-50 disabled:cursor-not-allowed transition-all hover-lift mt-2"
              >
                {isLoading ? "Création en cours..." : "S'inscrire"}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-muted-foreground">
              Déjà un compte ?{" "}
              <Link href="/login" className="font-medium text-primary hover:text-primary/80 transition-colors">
                Connectez-vous
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
