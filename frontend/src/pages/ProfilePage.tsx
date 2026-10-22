import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, Profile, Skill } from "../api";
import { signOut } from "../auth";

const levels = ["beginner", "intermediate", "advanced"];

export function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function load() {
    try { const [profileResult, skillsResult] = await Promise.all([api.get<Profile>("/profile/"), api.get<Skill[]>("/skills/")]); setProfile(profileResult.data); setSkills(skillsResult.data); }
    catch { signOut(); navigate("/login"); }
  }
  useEffect(() => { load(); }, []);

  async function updateProfile(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    try { const data = Object.fromEntries(new FormData(event.currentTarget)); const result = await api.put<Profile>("/profile/", data); setProfile(result.data); }
    catch { setError("Could not update your profile."); }
  }
  async function addSkill(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    try { await api.post("/user-skills/", Object.fromEntries(new FormData(event.currentTarget))); event.currentTarget.reset(); await load(); }
    catch (err: any) {
      const response = err.response?.data;
      setError(Array.isArray(response) ? response[0] : response?.detail || response?.non_field_errors?.[0] || "Could not add that skill.");
    }
  }
  async function removeSkill(id: number) { await api.delete(`/user-skills/${id}/`); await load(); }
  if (!profile) return <main className="loading">Loading your profile…</main>;

  return <main className="profile"><header><div><h1>TradeSwap</h1><p>Your skill-exchange profile</p></div><button className="secondary" onClick={() => { signOut(); navigate("/login"); }}>Sign out</button></header>
    <section className="card"><h2>About you</h2><form onSubmit={updateProfile} className="stack"><label>First name<input name="first_name" defaultValue={profile.first_name} /></label><label>Last name<input name="last_name" defaultValue={profile.last_name} /></label><label>Bio<textarea name="bio" defaultValue={profile.bio} placeholder="What do you enjoy teaching and learning?" /></label><button>Save profile</button></form></section>
    <section className="card"><h2>Add a skill</h2><form onSubmit={addSkill} className="skill-form"><label>Skill<select name="skill_id" required defaultValue=""><option value="" disabled>Select a skill</option>{skills.map(skill => <option key={skill.id} value={skill.id}>{skill.name}</option>)}</select></label><label>I want to<select name="direction" defaultValue="teach"><option value="teach">Teach</option><option value="learn">Learn</option></select></label><label>Level<select name="level" defaultValue="beginner">{levels.map(level => <option key={level} value={level}>{level}</option>)}</select></label><button>Add</button></form>{error && <p className="error">{error}</p>}</section>
    <section className="lists"><SkillList title="I can teach" skills={profile.teach_skills} removeSkill={removeSkill} /><SkillList title="I want to learn" skills={profile.learn_skills} removeSkill={removeSkill} /></section>
  </main>;
}

function SkillList({ title, skills, removeSkill }: { title: string; skills: Profile["teach_skills"]; removeSkill: (id: number) => void }) {
  return <section className="card"><h2>{title}</h2>{skills.length ? <ul>{skills.map(skill => <li key={skill.id}><span>{skill.skill_name}<small>{skill.level}</small></span><button className="icon" onClick={() => removeSkill(skill.id)} aria-label={`Remove ${skill.skill_name}`}>×</button></li>)}</ul> : <p className="muted">Nothing here yet.</p>}</section>;
}
