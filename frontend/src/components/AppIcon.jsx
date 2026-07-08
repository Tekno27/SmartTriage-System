import AlertTriangle from "lucide-react/dist/esm/icons/alert-triangle.mjs";
import BarChart3 from "lucide-react/dist/esm/icons/bar-chart-3.mjs";
import Bed from "lucide-react/dist/esm/icons/bed.mjs";
import Bell from "lucide-react/dist/esm/icons/bell.mjs";
import Brain from "lucide-react/dist/esm/icons/brain.mjs";
import Building2 from "lucide-react/dist/esm/icons/building-2.mjs";
import Calendar from "lucide-react/dist/esm/icons/calendar.mjs";
import Camera from "lucide-react/dist/esm/icons/camera.mjs";
import Check from "lucide-react/dist/esm/icons/check.mjs";
import CircleCheck from "lucide-react/dist/esm/icons/circle-check.mjs";
import CircleDollarSign from "lucide-react/dist/esm/icons/circle-dollar-sign.mjs";
import ClipboardList from "lucide-react/dist/esm/icons/clipboard-list.mjs";
import Clock from "lucide-react/dist/esm/icons/clock.mjs";
import Eye from "lucide-react/dist/esm/icons/eye.mjs";
import FileText from "lucide-react/dist/esm/icons/file-text.mjs";
import FlaskConical from "lucide-react/dist/esm/icons/flask-conical.mjs";
import FolderOpen from "lucide-react/dist/esm/icons/folder-open.mjs";
import Frown from "lucide-react/dist/esm/icons/frown.mjs";
import GraduationCap from "lucide-react/dist/esm/icons/graduation-cap.mjs";
import Hospital from "lucide-react/dist/esm/icons/hospital.mjs";
import Landmark from "lucide-react/dist/esm/icons/landmark.mjs";
import Meh from "lucide-react/dist/esm/icons/meh.mjs";
import Microscope from "lucide-react/dist/esm/icons/microscope.mjs";
import Package from "lucide-react/dist/esm/icons/package.mjs";
import Pill from "lucide-react/dist/esm/icons/pill.mjs";
import Receipt from "lucide-react/dist/esm/icons/receipt.mjs";
import Scan from "lucide-react/dist/esm/icons/scan.mjs";
import Scissors from "lucide-react/dist/esm/icons/scissors.mjs";
import Smile from "lucide-react/dist/esm/icons/smile.mjs";
import Sparkles from "lucide-react/dist/esm/icons/sparkles.mjs";
import Stethoscope from "lucide-react/dist/esm/icons/stethoscope.mjs";
import Ticket from "lucide-react/dist/esm/icons/ticket.mjs";
import UserRound from "lucide-react/dist/esm/icons/user-round.mjs";
import Wind from "lucide-react/dist/esm/icons/wind.mjs";
import X from "lucide-react/dist/esm/icons/x.mjs";
import Thermometer from "lucide-react/dist/esm/icons/thermometer.mjs";
import Activity from "lucide-react/dist/esm/icons/activity.mjs";
import Bandage from "lucide-react/dist/esm/icons/bandage.mjs";
import Ear from "lucide-react/dist/esm/icons/ear.mjs";
import Droplets from "lucide-react/dist/esm/icons/droplets.mjs";
import Bone from "lucide-react/dist/esm/icons/bone.mjs";
import HeartPulse from "lucide-react/dist/esm/icons/heart-pulse.mjs";
import ShieldAlert from "lucide-react/dist/esm/icons/shield-alert.mjs";
import Snowflake from "lucide-react/dist/esm/icons/snowflake.mjs";

export const ICONS = {
  hospital: Hospital,
  stethoscope: Stethoscope,
  doctor: UserRound,
  reception: Bell,
  calendar: Calendar,
  bed: Bed,
  wards: Building2,
  theatre: Scissors,
  laboratory: FlaskConical,
  radiology: Scan,
  pharmacy: Pill,
  inventory: Package,
  billing: CircleDollarSign,
  reports: BarChart3,
  records: FolderOpen,
  student: GraduationCap,
  ticket: Ticket,
  clipboard: ClipboardList,
  clock: Clock,
  alert: AlertTriangle,
  sparkles: Sparkles,
  check: Check,
  circleCheck: CircleCheck,
  x: X,
  camera: Camera,
  microscope: Microscope,
  receipt: Receipt,
  landmark: Landmark,
  file: FileText,
  thermometer: Thermometer,
  brain: Brain,
  activity: Activity,
  wind: Wind,
  heartPulse: HeartPulse,
  eye: Eye,
  bandage: Bandage,
  ear: Ear,
  droplets: Droplets,
  bone: Bone,
  shieldAlert: ShieldAlert,
  snowflake: Snowflake,
  smile: Smile,
  meh: Meh,
  frown: Frown,
};

export const SYMPTOM_ICON_MAP = {
  fever: "thermometer",
  headache: "brain",
  stomach_pain: "activity",
  nausea_vomiting: "wind",
  cough: "wind",
  sore_throat: "wind",
  chest_pain: "heartPulse",
  difficulty_breathing: "wind",
  dizziness: "brain",
  body_aches: "activity",
  runny_nose: "wind",
  rash: "activity",
  diarrhoea: "droplets",
  ear_pain: "ear",
  eye_irritation: "eye",
  fatigue: "activity",
  back_pain: "bone",
  injury_trauma: "bandage",
  allergic_reaction: "shieldAlert",
  chills: "snowflake",
};

export default function AppIcon({ name, size = 18, className, strokeWidth = 2 }) {
  const Icon = ICONS[name];
  if (!Icon) return null;
  return <Icon size={size} className={className} strokeWidth={strokeWidth} aria-hidden />;
}

export function SymptomIcon({ symptomId, size = 22, className }) {
  const iconName = SYMPTOM_ICON_MAP[symptomId] || "activity";
  return <AppIcon name={iconName} size={size} className={className} />;
}
