import React, { useState, useEffect, useRef, useContext, createContext, useMemo } from 'react';
import { 
  Menu, X, ArrowRight, ChevronRight, TrendingUp, Shield, 
  Zap, Globe, Search, RefreshCw, Layers, CheckCircle, 
  Lock, Activity, FileText, Plus, Users, Fingerprint,
  Building2, Wallet, FileCheck, Ghost, Skull, Flame, Github, Twitter, Linkedin
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';


/* --- 1. New Logo Component --- */
const DarkLedgerLogo = ({ className }) => (
  <svg 
    viewBox="0 0 400 400" 
    className={className} 
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-label="DarkLedger Logo"
  >
    <defs>
        {/* Included the base64 image data from your file */}
        <image width="400" height="400" id="img1" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQCAMAAAC3Ycb+AAAAAXNSR0IB2cksfwAAAv1QTFRF/////Pz82NjYrKysg4ODbm5uampqZWVlYWFhYGBgZmZmb29vd3d3hISEo6OjxsbG6Ojo/v7+8/PzycnJnZ2deXl5bGxsaGhoZGRkaWlpcnJyenp6jY2Nr6+v0tLS+fn5wsLCRkZGDAwMAAAAFxcXXl5epaWl6urq6+vrrq6uMDAwAgICLi4udnZ2vb29ysrKQkJCn5+f8vLy9/f3ra2tUVFRBgYGDg4OYmJiv7+//f39mpqaKCgoCgoKXFxc1NTU5eXlEBAQHh4e7+/v7u7uh4eHGxsbAQEBTU1NwcHBc3Nz5OTkICAgWlpa5ubm9fX1BwcHjo6O+/v75+fnR0dHk5OTurq6HR0dLy8vw8PDGBgYUlJS8fHxf39/mJiYKSkp1dXVQEBAXV1dDw8P29vbJCQkOjo67Ozs9PT0SkpKqKiozs7O39/f9vb2Ozs7z8/PGRkZ3d3dTExMAwMD2traFhYWISEhvr6+j4+PExMT4+PjUFBQJSUlBQUFy8vLLCws+vr6Nzc3fX19jIyMOTk52dnZDQ0Nq6urHBwc+Pj4U1NTMTExl5eX1tbWCQkJtbW1X19fcXFxPz8/qampBAQET09Pp6enioqKSUlJ6enpoaGhERERZ2dnJycnJiYmlZWVzc3NbW1txcXFgoKCe3t7a2trQ0NDgYGBODg4WVlZKysrfn5+VFRUhYWFPT09RUVFoKCgLS0thoaGVVVVkZGRubm50dHRsLCwx8fHGhoat7e3FRUV3NzcNjY2V1dXcHBwHx8fdXV1CAgI3t7eVlZWnJycCwsLREREkpKSuLi4NTU1MjIyPj4+iYmJTk5OlpaW7e3tdHR0FBQUIyMjxMTEpKSkfHx8lJSUEhISoqKiiIiIeHh44uLisbGx4ODg09PT19fXtra2mZmZSEhIMzMzwMDAkJCQqqqqyMjInp6es7OzWFhYgICANDQ0u7u78PDwvLy8IiIipqam4eHhW1tb0NDQi4uLY2NjQUFBS0tLzMzMm5ubKioqsrKyPDw8rmbhaQAAAP90Uk5TAAAA////////////////bQAAAFr/////////////IACG////////AAD//////6ZT//8AAP//////mgD/////FAD//wAA/////43/AP//AAD//wAA//+5//+A//8A////Df///wD//wAA//86AAD/M/8A//8A//+g//8A////Tf8A/////wD///8A////B//Z////////////AP///////0D/c////////////////////////8An+Wb/zf8A////////AP//////xv///////wD///96/////////wDzABoA0////5P//2D/5v///7MArf//AP8t/////0f//+z/knFiNQAAH3FJREFUeJztnXlAFVX7x2esFHcQrEQTU0w0idzKfDV3801NuriS+4ohIq6IS7iQaS6oibkhSoZbablmariVuOJrpr6ZC1aaae6m/lJe4DLLvczcWc7znJnfnfv5I0Y48+Wh7713Zs55zvOwjAdTwRodgAdHPIaYDI8hJsNjiMnwGGIyPIaYDI8hJsNjiMnwGGIyPIaYDI8hJsNjiMnwGGIyPIaYDI8hJsNjiMnwGGIyPIaYDI8hJsNjiMnwGGIyPIaYDI8hJsNjiMnwGGIyPIaYDI8hJsNjiMnwGGIyqBvCOnODdgRKlLHHdSvbJ+/r3b+o/naqhgSw1/1Yp9+Y+zefoRmES4LYrAD2geP3iuaYc5FaBBQNCTlbLlvyB17PsOxRenHIUifntXFd8ic5LyP2ezpB0DIkoAJ72cWP/Vl2N6VI5Giyv2GWix8H7Gm8k0YYdAxpwbK/KAwJZNmtVGKRpuKfwdJvDoHsIHYzfiBUDKle5ZSaYTXYr7EjkaH94XonVAzz82e/xA6FgiFh7DGVI/0qPkb/g6XoxB5WObIem4YaCQ1DOj2doX5wffYzvEhksBU/+kB5VD6+QSsQQ2HwDWG7afhrc2jIpiBFIkdYqT2axje+/hVSJHkgG2K79pvGM5r89ANKJHL0Y3dpPKM5uxAlEju4hkSw2zWfE+yfhBCJHJE3NHyg5lPu1U8QIskH1ZAoffeJt65BByJL9AE9v6sdOxs8Eg5MQ2yV9H3ahiY+Bo5EjhE6b2PDDqbDBiKAaIjPA3+dZ/o2nQYaiRzeA77QeWa9P7Ee2xENiV2r+9RO7IeAgcjBRul/8u6ShDRLjWdI9A9KcxEuaPMrhSfE7iTzhR0/AovDATRDIvyInmn/uAsViCyvPNb0hOREeBLB680FaIYUf57o9NDik4ACkaN9Nb0XEDvd2HiYQBzBMqRi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" />
    </defs>
    <use id="Background" href="#img1" x="0" y="0" />
  </svg>
);






/* --- Theme Context --- */

const ThemeContext = createContext({
  isSpooky: false,
  toggleTheme: () => {}
});

const useTheme = () => useContext(ThemeContext);

/* --- Animation Utilities --- */

const useScrollAnimation = () => {
  const [isVisible, setIsVisible] = useState(false);
  const domRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          if (domRef.current) observer.unobserve(domRef.current);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    const current = domRef.current;
    if (current) observer.observe(current);

    return () => {
      if (current) observer.unobserve(current);
    };
  }, []);

  return { isVisible, domRef };
};

const FadeIn = ({ children, delay = 0, className = "" }: { children?: React.ReactNode, delay?: number, className?: string }) => {
  const { isVisible, domRef } = useScrollAnimation();
  return (
    <div
      ref={domRef}
      className={`transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] transform ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'
      } ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};

/* --- Components --- */

/* --- 2. Updated Navbar --- */
const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isSpooky, toggleTheme } = useTheme();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navBgClass = isSpooky 
    ? (isScrolled ? 'bg-black/90 backdrop-blur-md border-b border-red-900/30' : 'bg-transparent py-6')
    : (isScrolled ? 'bg-white/80 backdrop-blur-md py-4 border-b border-gray-100' : 'bg-transparent py-6');

  const textColor = isSpooky ? 'text-gray-400 hover:text-spooky-accent' : 'text-gray-600 hover:text-black';
  const logoColor = isSpooky ? 'text-spooky-accent' : 'text-duna-900';
  const buttonClass = isSpooky 
    ? 'bg-spooky-accent text-white hover:bg-red-700 shadow-red-900/50' 
    : 'bg-duna-900 text-white hover:bg-gray-800 shadow-gray-200';

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${navBgClass}`}>
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        
        {/* --- Logo Section Updated --- */}
        <div className="flex items-center gap-3">
          {/* Replaced the skull icon/text conditional logic with the new Logo Component */}
          {/* I added CSS filters to the logo when in Spooky mode so it matches the red aesthetic */}
          <DarkLedgerLogo 
            className={`w-10 h-10 transition-all duration-500 ${isSpooky ? 'brightness-125 sepia-[.5] hue-rotate-[-50deg] drop-shadow-[0_0_8px_rgba(220,38,38,0.6)]' : ''}`} 
          />
          <span className={`text-2xl font-bold tracking-tighter transition-colors ${logoColor} ${isSpooky ? 'font-spooky text-3xl tracking-widest' : ''}`}>
            DARKLEDGER
          </span>
        </div>

        <div className={`hidden md:flex items-center space-x-8 text-sm font-medium transition-colors ${isSpooky ? 'text-gray-400' : 'text-gray-600'}`}>
          <a href="#" className={`transition-colors ${textColor}`}>Product</a>
          <a href="#" className={`transition-colors ${textColor}`}>Customers</a>
          <a href="#" className={`transition-colors ${textColor}`}>Company</a>
          <a href="#" className={`transition-colors ${textColor}`}>Resources</a>
        </div>

        <div className="hidden md:flex items-center gap-4">
          <button 
            onClick={toggleTheme}
            className={`p-2 rounded-full transition-all duration-500 hover:scale-110 ${isSpooky ? 'bg-red-900/30 text-red-500 border border-red-900/50' : 'bg-gray-100 text-gray-600'}`}
            title="Toggle Theme"
          >
             {isSpooky ? '💀' : '👻'}
          </button>
          <button className={`px-5 py-2.5 rounded-full text-sm font-medium transition-colors shadow-lg ${buttonClass}`}>
            {isSpooky ? 'Summon a Demo' : 'Request Access'}
          </button>
        </div>

        <div className="flex items-center gap-4 md:hidden">
          <button 
              onClick={toggleTheme}
              className={`p-2 rounded-full transition-all ${isSpooky ? 'bg-red-900/30 text-red-500' : 'bg-gray-100 text-gray-600'}`}
            >
              {isSpooky ? '💀' : '👻'}
          </button>
          <button className={isSpooky ? 'text-white' : 'text-black'} onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className={`md:hidden absolute top-full left-0 right-0 border-b p-6 flex flex-col space-y-4 shadow-lg animate-in slide-in-from-top-5 ${isSpooky ? 'bg-black border-red-900 text-white' : 'bg-white border-gray-100 text-black'}`}>
          <a href="#" className="text-lg font-medium">Product</a>
          <a href="#" className="text-lg font-medium">Customers</a>
          <a href="#" className="text-lg font-medium">Company</a>
          <a href="#" className="text-lg font-medium">Resources</a>
          <button className={`px-5 py-3 rounded-full text-base font-medium w-full ${buttonClass}`}>
            {isSpooky ? 'Summon a Demo' : 'Request Access'}
          </button>
        </div>
      )}
    </nav>
  );
};

const Hero = () => {
  const parallaxRef = useRef<HTMLDivElement>(null);
  const { isSpooky } = useTheme();

  useEffect(() => {
    const handleScroll = () => {
      if (parallaxRef.current) {
        const yOffset = window.scrollY * 0.3;
        parallaxRef.current.style.transform = `translate3d(0, ${yOffset}px, 0)`;
      }
    };
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const heroImage = isSpooky 
    ? "https://res.cloudinary.com/djfvylf6b/image/upload/v1764964367/Gemini_Generated_Image_lindp4lindp4lind_h8kpfo.png?q=80&w=3270&auto=format&fit=crop" 
    : "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=3270&auto=format&fit=crop"; 

  const gradientOverlay = isSpooky
    ? "bg-gradient-to-b from-black/70 via-black/80 to-black"
    : "bg-gradient-to-b from-white/70 via-white/50 to-[#FAFAFA]";

  const textColor = isSpooky ? 'text-spooky-accent' : 'text-duna-900';
  const subtextColor = isSpooky ? 'text-gray-400' : 'text-gray-600';
  const buttonClass = isSpooky 
    ? 'bg-spooky-accent text-white hover:bg-red-800 shadow-red-900/40' 
    : 'bg-duna-900 text-white hover:bg-black';

  return (
    <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden min-h-[800px] flex flex-col justify-center transition-colors duration-500">
      {/* Background Image Wrapper */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <div 
            ref={parallaxRef}
            className="absolute -top-[30%] left-0 w-full h-[160%] z-0 will-change-transform transition-all duration-1000"
        >
            <img 
              src={heroImage} 
              alt="Background" 
              className={`w-full h-full object-cover object-center transition-opacity duration-1000 ${isSpooky ? 'opacity-50 grayscale-[80%] brightness-75' : 'opacity-90'}`}
            />
        </div>
        <div className={`absolute inset-0 z-10 transition-all duration-1000 ${gradientOverlay}`}></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 text-center mt-10">
        <FadeIn>
          <h1 className={`text-5xl md:text-7xl font-semibold tracking-tighter mb-6 leading-[1.05] transition-colors ${textColor} ${isSpooky ? 'font-spooky tracking-widest drop-shadow-[0_4px_10px_rgba(220,20,60,0.5)]' : ''}`}>
            {isSpooky ? (
              <>The new standard in <br /> "Dead" Tech Compliance.</>
            ) : (
              <>The new standard in <br /> Algorithmic Payroll.</>
            )}
          </h1>
        </FadeIn>
        
        <FadeIn delay={100}>
          <p className={`text-xl md:text-2xl max-w-2xl mx-auto mb-10 font-light tracking-tight transition-colors ${subtextColor}`}>
            {isSpooky 
              ? "Meet the hybrid platform that stitches 1970s mainframe precision with 2025 Web3 speed. Audit-proof payroll for the undead enterprise."
              : "The first hybrid platform that merges the precision of mainframe banking with the speed of Web3 settlement. Audit-proof compliance for the modern enterprise."}
          </p>
        </FadeIn>

        <FadeIn delay={200}>
          <button className={`px-8 py-4 rounded-full text-lg font-medium transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl ${buttonClass}`}>
            {isSpooky ? 'Summon a Demo' : 'Request Access'}
          </button>
        </FadeIn>

        <div className="mt-20">
          <FadeIn delay={300}>
            <p className={`text-xs font-semibold uppercase tracking-widest mb-8 ${isSpooky ? 'text-red-900' : 'text-gray-500'}`}>
              {isSpooky ? 'Built for businesses where "floating point errors" are a fatal sin' : 'Trusted by organizations where "floating point errors" are unacceptable'}
            </p>
            
            {/* LOGOS SECTION */}
            <div className={`flex flex-wrap justify-center items-center gap-12 md:gap-20 transition-all duration-500 ${isSpooky ? 'text-gray-500 opacity-60 grayscale brightness-75 contrast-150' : 'text-black opacity-80 grayscale hover:grayscale-0'}`}>
              
              {/* COBOL PNG */}
              <div className="h-10 md:h-12 group relative" title="COBOL Core">
                 <img 
                   src="https://cdn.prod.website-files.com/6047a9e35e5dc54ac86ddd90/63018724eab2481fa8f88ef4_1d1684aa.png" 
                   alt="COBOL" 
                   className={`h-full w-auto object-contain transition-all duration-500 ${isSpooky ? 'invert' : ''}`}
                 />
                 {isSpooky && <span className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 text-[10px] bg-red-900 text-white p-1 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap">Legacy Strength</span>}
              </div>

              {/* PYTHON PNG */}
              <div className="h-10 md:h-12 group relative" title="Python Orchestration">
                  <img 
                    src="https://cdn-icons-png.flaticon.com/512/5968/5968286.png" 
                    alt="Python" 
                    className={`h-full w-auto object-contain transition-all duration-500 ${isSpooky ? 'invert' : ''}`} 
                  />
                  {isSpooky && <span className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 text-[10px] bg-red-900 text-white p-1 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap">Snake Charmers</span>}
              </div>

              {/* COINBASE SVG */}
              <div className="h-12 md:h-14 group relative" title="Coinbase Settlement">
                <svg viewBox="0 0 24 24" className="h-full w-auto fill-current">
                    <path d="M4.844 11.053c-0.872 0 -1.553 0.662 -1.553 1.548s0.664 1.542 1.553 1.542c0.889 0 1.564 -0.667 1.564 -1.547 0 -0.875 -0.664 -1.543 -1.564 -1.543zm0.006 2.452c-0.497 0 -0.86 -0.386 -0.86 -0.904 0 -0.523 0.357 -0.909 0.854 -0.909 0.502 0 0.866 0.392 0.866 0.91 0 0.517 -0.364 0.903 -0.86 0.903zm1.749 -1.778h0.433v2.36h0.693V11.11H6.599zm-5.052 -0.035c0.364 0 0.653 0.224 0.762 0.558h0.734c-0.133 -0.713 -0.722 -1.197 -1.49 -1.197 -0.872 0 -1.553 0.662 -1.553 1.548 0 0.887 0.664 1.543 1.553 1.543 0.75 0 1.351 -0.484 1.484 -1.203h-0.728a0.78 0.78 0 0 1 -0.756 0.564c-0.502 0 -0.855 -0.386 -0.855 -0.904 0 -0.523 0.347 -0.909 0.85 -0.909zm18.215 0.622 -0.508 -0.075c-0.242 -0.035 -0.415 -0.115 -0.415 -0.305 0 -0.207 0.225 -0.31 0.53 -0.31 0.336 0 0.55 0.143 0.595 0.379h0.67c-0.075 -0.599 -0.537 -0.95 -1.247 -0.95 -0.733 0 -1.218 0.375 -1.218 0.904 0 0.506 0.317 0.8 0.958 0.892l0.508 0.075c0.249 0.034 0.387 0.132 0.387 0.316 0 0.236 -0.242 0.334 -0.577 0.334 -0.41 0 -0.641 -0.167 -0.676 -0.42h-0.681c0.064 0.581 0.52 0.99 1.35 0.99 0.757 0 1.26 -0.346 1.26 -0.938 0 -0.53 -0.364 -0.806 -0.936 -0.892zM7.378 9.885a0.429 0.429 0 0 0 -0.444 0.437c0 0.254 0.19 0.438 0.444 0.438a0.429 0.429 0 0 0 0.445 -0.438 0.429 0.429 0 0 0 -0.445 -0.437zm10.167 2.245c0 -0.645 -0.392 -1.076 -1.224 -1.076 -0.785 0 -1.224 0.397 -1.31 1.007h0.687c0.035 -0.236 0.22 -0.432 0.612 -0.432 0.352 0 0.525 0.155 0.525 0.345 0 0.248 -0.317 0.311 -0.71 0.351 -0.531 0.058 -1.19 0.242 -1.19 0.933 0 0.535 0.4 0.88 1.034 0.88 0.497 0 0.809 -0.207 0.965 -0.535 0.023 0.293 0.242 0.483 0.548 0.483h0.404v-0.616h-0.34v-1.34zm-0.68 0.748c0 0.397 -0.347 0.69 -0.769 0.69 -0.26 0 -0.48 -0.11 -0.48 -0.34 0 -0.293 0.353 -0.373 0.676 -0.408 0.312 -0.028 0.485 -0.097 0.572 -0.23zm-3.679 -1.825c-0.386 0 -0.71 0.162 -0.94 0.432V9.856h-0.693v4.23h0.68v-0.391c0.232 0.282 0.56 0.449 0.953 0.449 0.832 0 1.461 -0.656 1.461 -1.543 0 -0.886 -0.64 -1.548 -1.46 -1.548zm-0.103 2.452c-0.497 0 -0.86 -0.386 -0.86 -0.904 0 -0.517 0.369 -0.909 0.865 -0.909 0.503 0 0.855 0.386 0.855 0.91 0 0.517 -0.364 0.903 -0.86 0.903zm-3.187 -2.452c-0.45 0 -0.745 0.184 -0.919 0.443v-0.385H8.29v2.975h0.693v-1.617c0 -0.455 0.289 -0.777 0.716 -0.777 0.398 0 0.647 0.282 0.647 0.69v1.704h0.692v-1.755c0 -0.748 -0.386 -1.278 -1.142 -1.278zM24 12.503c0 -0.851 -0.624 -1.45 -1.46 -1.45 -0.89 0 -1.542 0.668 -1.542 1.548 0 0.927 0.698 1.543 1.553 1.543 0.722 0 1.287 -0.426 1.432 -1.03h-0.722c-0.104 0.264 -0.358 0.414 -0.699 0.414 -0.445 0 -0.78 -0.276 -0.854 -0.76H24v-0.264zm-2.252 -0.23c0.11 -0.414 0.422 -0.615 0.78 -0.615 0.392 0 0.693 0.224 0.762 0.615Z" />
                </svg>
                 {isSpooky && <span className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 text-[10px] bg-red-900 text-white p-1 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap">Crypto Native</span>}
              </div>

            </div>
          </FadeIn>
        </div>
      </div>
    </section>
  );
};

const Stats = () => {
  const { isSpooky } = useTheme();
  
  return (
    <section className={`py-20 transition-colors duration-500 ${isSpooky ? 'bg-black' : 'bg-[#FAFAFA]'}`}>
      <div className="max-w-7xl mx-auto px-6">
        <div className={`grid grid-cols-1 md:grid-cols-3 gap-12 border-b pb-20 ${isSpooky ? 'border-red-900/20' : 'border-gray-200'}`}>
          <div>
            <div className={`text-5xl font-semibold tracking-tighter mb-2 ${isSpooky ? 'text-spooky-accent font-spooky tracking-widest' : 'text-duna-900'}`}>
                100%
            </div>
            <div className={`${isSpooky ? 'text-gray-500' : 'text-gray-500'} font-medium tracking-tight`}>
                Decimal Accuracy (Zero Float Drift)
            </div>
          </div>
          <div>
            <div className={`text-5xl font-semibold tracking-tighter mb-2 ${isSpooky ? 'text-spooky-accent font-spooky tracking-widest' : 'text-duna-900'}`}>
                {isSpooky ? '0.0s' : '< 1s'}
            </div>
            <div className={`${isSpooky ? 'text-gray-500' : 'text-gray-500'} font-medium tracking-tight`}>
                Settlement Time (Base L2)
            </div>
          </div>
          <div>
            <div className={`text-5xl font-semibold tracking-tighter mb-2 ${isSpooky ? 'text-spooky-accent font-spooky tracking-widest' : 'text-duna-900'}`}>
                {isSpooky ? '60+' : '40+'}
            </div>
            <div className={`${isSpooky ? 'text-gray-500' : 'text-gray-500'} font-medium tracking-tight`}>
                {isSpooky ? 'Years of Proven Math (COBOL)' : 'Years of Proven Logic (COBOL Core)'}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const ValueProps = () => {
  const { isSpooky } = useTheme();
  
  const iconBg = isSpooky ? 'bg-spooky-card border-red-900/40 text-spooky-accent' : 'bg-white border-gray-100 group-hover:bg-sand text-gray-700';
  const headingColor = isSpooky ? 'text-spooky-accent' : 'text-duna-900';
  const textColor = isSpooky ? 'text-gray-500' : 'text-gray-600';

  return (
    <section className={`py-12 transition-colors duration-500 ${isSpooky ? 'bg-black' : 'bg-[#FAFAFA]'}`}>
      <div className="max-w-7xl mx-auto px-6">
        <FadeIn>
          <h2 className={`text-4xl md:text-5xl font-semibold tracking-tighter mb-16 ${headingColor} ${isSpooky ? 'font-spooky tracking-wider' : ''}`}>
            {isSpooky ? 'Designed to Terrify. Built to Verify.' : 'Engineered for Accuracy. Built for Speed.'}
          </h2>
        </FadeIn>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          <FadeIn delay={100} className="h-full">
            <div className="group h-full flex flex-col">
              <div className={`mb-6 inline-block p-3 border shadow-sm rounded-xl transition-colors w-fit ${iconBg}`}>
                {isSpooky ? <Skull className="w-6 h-6" /> : <TrendingUp className="w-6 h-6" />}
              </div>
              <h3 className={`text-xl font-semibold mb-3 tracking-tight ${isSpooky ? 'text-gray-200' : ''}`}>
                {isSpooky ? 'Drive Revenue with Dead Tech' : 'The Precision Engine'}
              </h3>
              <p className="text-sm font-semibold uppercase tracking-wider mb-2 opacity-50">
                  {isSpooky ? 'Resurrection Engine' : 'Bank-Grade Math'}
              </p>
              <p className={`${textColor} leading-relaxed`}>
                {isSpooky 
                  ? "We don't trust modern math. Our core engine is built on GnuCOBOL, the same technology powering 95% of the world's ATM swipes. It's not obsolete; it's immortal."
                  : "Modern languages suffer from binary approximation errors. We run core logic on GnuCOBOL—the same fixed-point technology powering 95% of the world's ATM swipes. It’s not legacy; it’s the standard."}
              </p>
            </div>
          </FadeIn>
          
          <FadeIn delay={200} className="h-full">
            <div className="group h-full flex flex-col">
              <div className={`mb-6 inline-block p-3 border shadow-sm rounded-xl transition-colors w-fit ${iconBg}`}>
                {isSpooky ? <Ghost className="w-6 h-6" /> : <Lock className="w-6 h-6" />}
              </div>
              <h3 className={`text-xl font-semibold mb-3 tracking-tight ${isSpooky ? 'text-gray-200' : ''}`}>
                {isSpooky ? 'Future-Proof Stitching' : 'Hybrid Architecture'}
              </h3>
              <p className="text-sm font-semibold uppercase tracking-wider mb-2 opacity-50">
                  {isSpooky ? 'The Frankenstein Stitch' : 'Seamless Interoperability'}
              </p>
              <p className={`${textColor} leading-relaxed`}>
                {isSpooky 
                 ? "A powerful Python Bridge connects our legacy brain to the Base L2 blockchain. We stitched the incompatible to create the undeniable."
                 : "Our proprietary Python Bridge orchestrates a secure handshake between the legacy calculation engine and the blockchain, translating JSON to fixed-width records in milliseconds."}
              </p>
            </div>
          </FadeIn>

          <FadeIn delay={300} className="h-full">
            <div className="group h-full flex flex-col">
              <div className={`mb-6 inline-block p-3 border shadow-sm rounded-xl transition-colors w-fit ${iconBg}`}>
                {isSpooky ? <Flame className="w-6 h-6" /> : <Zap className="w-6 h-6" />}
              </div>
              <h3 className={`text-xl font-semibold mb-3 tracking-tight ${isSpooky ? 'text-gray-200' : ''}`}>
                {isSpooky ? 'Eliminate Gas Fees' : 'Global Settlement'}
              </h3>
              <p className="text-sm font-semibold uppercase tracking-wider mb-2 opacity-50">
                  {isSpooky ? 'Reduce Sacrifice' : 'Instant Payouts'}
              </p>
              <p className={`${textColor} leading-relaxed`}>
                {isSpooky 
                 ? "Stop sacrificing your runway to the Ethereum mainnet. Our Coinbase SDK integration ensures gasless, instant USDC settlement for every minion on your payroll."
                 : "Bypass traditional banking delays. Our Coinbase SDK integration enables gas-optimized, instant USDC settlement on the Base L2 network for employees worldwide."}
              </p>
            </div>
          </FadeIn>
        </div>
      </div>
    </section>
  );
};

const Testimonials = () => {
  const { isSpooky } = useTheme();
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: 'left' | 'right') => {
    if (scrollContainerRef.current) {
        const scrollAmount = direction === 'left' ? -400 : 400;
        scrollContainerRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <section className={`py-24 transition-colors duration-500 ${isSpooky ? 'bg-black' : 'bg-[#FAFAFA]'}`}>
      <div className="max-w-7xl mx-auto px-6">
        <FadeIn>
          <div className="flex justify-between items-end mb-12">
            <div>
                <h2 className={`text-4xl font-semibold tracking-tighter mb-4 ${isSpooky ? 'text-spooky-accent font-spooky' : 'text-duna-900'}`}>
                    {isSpooky ? 'Run your startup like a ruthless Overlord.' : 'The infrastructure behind accurate decisions.'}
                </h2>
                <p className={`${isSpooky ? 'text-gray-500' : 'text-gray-600'} max-w-xl`}>
                  {isSpooky ? 'Run your dungeon like the underworld\'s best overlords.' : 'Trusted by leaders who value precision over approximation.'}
                </p>
            </div>
            <div className="flex gap-2">
                <button onClick={() => scroll('left')} className={`p-3 rounded-full border transition-all hover:scale-105 ${isSpooky ? 'border-red-900 text-red-700 hover:bg-red-950' : 'border-gray-200 text-gray-500 hover:bg-gray-50'}`}>
                    <ChevronRight size={20} className="rotate-180"/>
                </button>
                <button onClick={() => scroll('right')} className={`p-3 rounded-full border transition-all hover:scale-105 ${isSpooky ? 'border-red-900 text-red-700 hover:bg-red-950' : 'border-gray-200 text-gray-500 hover:bg-gray-50'}`}>
                    <ChevronRight size={20}/>
                </button>
            </div>
          </div>
        </FadeIn>

        {/* Carousel Container */}
        <div 
            ref={scrollContainerRef}
            className="flex gap-6 overflow-x-auto snap-x snap-mandatory hide-scrollbar pb-10 -mx-6 px-6 md:px-0 md:mx-0"
            style={{ 
                scrollPaddingLeft: '0px', 
            }}
        >
          
          {/* Card 1: Qonto */}
          <div className="snap-center shrink-0 w-[85vw] md:w-[450px] h-[400px]">
             <div className={`${isSpooky ? 'bg-spooky-card border-red-900/30 border' : 'bg-sand'} rounded-3xl p-8 flex flex-col justify-center items-center relative group overflow-hidden transition-all hover:shadow-lg h-full w-full`}>
               <span className={`text-3xl font-bold z-10 ${isSpooky ? 'text-gray-200' : 'text-gray-800'}`}>Qonto</span>
               <div className="absolute bottom-4 right-4 bg-white/50 w-10 h-10 rounded-full flex items-center justify-center transition-transform group-hover:scale-110 cursor-pointer">
                  <Plus size={20} />
               </div>
               {isSpooky && <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-red-900/10 to-transparent opacity-50"></div>}
            </div>
          </div>

          {/* Card 2: Remote Profile */}
          <div className="snap-center shrink-0 w-[85vw] md:w-[450px] h-[400px]">
            <div className={`${isSpooky ? 'bg-[#0a0a0a] border border-red-900/40' : 'bg-duna-900'} rounded-3xl relative overflow-hidden group transition-all hover:shadow-xl h-full w-full`}>
              <img 
                src="https://images.unsplash.com/photo-1556157382-97eda2d62296?q=80&w=2940&auto=format&fit=crop" 
                alt="Person" 
                className={`w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ${isSpooky ? 'opacity-30 grayscale contrast-125 sepia' : 'opacity-80'}`}
              />
              <div className="absolute bottom-0 left-0 p-8 text-white w-full bg-gradient-to-t from-black/90 to-transparent">
                  <div className="flex items-center gap-2 mb-2">
                      <div className="bg-white/20 p-1 rounded backdrop-blur-md">
                          <Globe size={16} className="text-white"/>
                      </div>
                      <span className="font-bold tracking-tight">remote</span>
                  </div>
              </div>
            </div>
          </div>

          {/* Card 3: Plaid/Necro-Finance Quote */}
           <div className="snap-center shrink-0 w-[85vw] md:w-[450px] h-[400px]">
             <div className={`${isSpooky ? 'bg-[#1a0505] border border-red-900/50' : 'bg-[#B7956B]'} rounded-3xl p-10 relative overflow-hidden flex flex-col justify-between text-white shadow-lg group transition-all hover:shadow-xl h-full w-full`}>
               <div className="absolute inset-0 bg-gradient-to-tr from-black/50 to-transparent"></div>
               <div className="relative z-10 flex justify-between items-start">
                   <div>
                      <p className="text-base font-medium opacity-90">Zak Lambert</p>
                      <p className="text-xs opacity-75 uppercase tracking-wide">
                        {isSpooky ? 'GM, Necro-Finance' : 'CFO, FinScale'}
                      </p>
                   </div>
                   <span className="font-bold tracking-widest text-lg">
                    {isSpooky ? 'NECRO' : 'FinScale'}
                   </span>
               </div>
               <blockquote className={`relative z-10 text-xl md:text-2xl font-medium leading-relaxed mt-4 tracking-tight ${isSpooky ? 'text-red-100/80' : ''}`}>
                   "{isSpooky 
                    ? 'Payroll used to be a guessing game with JavaScript math. Now, it\'s dead accurate thanks to DarkLedger\'s COBOL core.' 
                    : 'Payroll audits used to be a nightmare of rounding errors. DarkLedger\'s fixed-point engine balanced our books to the cent instantly.'}"
               </blockquote>
            </div>
          </div>

          {/* Card 4: Stripe/Ghost_Stripe Quote */}
           <div className="snap-center shrink-0 w-[85vw] md:w-[450px] h-[400px]">
             <div className={`${isSpooky ? 'bg-[#0f0f0f] border border-gray-800' : 'bg-[#7A8C43]'} rounded-3xl p-10 relative overflow-hidden flex flex-col justify-end text-white shadow-lg group transition-all hover:shadow-xl h-full w-full`}>
               <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop" className="absolute inset-0 object-cover opacity-60 mix-blend-overlay group-hover:scale-105 transition-transform duration-1000" alt="texture"/>
               <div className="relative z-10 mb-auto flex justify-between items-start w-full">
                   <div>
                      <p className="text-base font-medium opacity-90">David Singleton</p>
                      <p className="text-xs opacity-75 uppercase tracking-wide">
                        {isSpooky ? 'Former CTO, Ghost_Stripe' : 'CTO, ChainPay'}
                      </p>
                   </div>
                   <span className="font-bold italic text-lg">ChainPay</span>
               </div>
               <blockquote className={`relative z-10 text-xl md:text-2xl font-medium leading-relaxed tracking-tight ${isSpooky ? 'text-gray-300' : ''}`}>
                   "{isSpooky 
                    ? 'I thought COBOL was dead. DarkLedger proved it was just sleeping. The precision is spooky.' 
                    : 'The perfect bridge between the stability of traditional finance and the velocity of crypto. It just works.'}"
               </blockquote>
            </div>
          </div>

          {/* Card 5: seQura */}
           <div className="snap-center shrink-0 w-[85vw] md:w-[450px] h-[400px]">
            <div className={`${isSpooky ? 'bg-black border border-gray-900' : 'bg-duna-800'} rounded-3xl p-8 flex flex-col justify-center items-center relative text-white transition-all hover:shadow-lg group h-full w-full`}>
               <span className="text-2xl font-bold">seQura</span>
               <div className="absolute bottom-4 right-4 bg-white/20 w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-transform group-hover:scale-110 cursor-pointer">
                  <Plus size={20} />
               </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

const Infrastructure = () => {
  const { isSpooky } = useTheme();

  return (
    <section className={`py-32 transition-colors duration-500 border-y ${isSpooky ? 'bg-black border-red-900/10' : 'bg-sand/30 border-sand-dark/50'}`}>
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
            <div>
                <h2 className={`text-4xl font-semibold tracking-tighter mb-6 ${isSpooky ? 'text-spooky-accent font-spooky' : 'text-duna-900'}`}>
                  {isSpooky ? 'The anatomy of a Monster.' : 'A Chimera of Stability and Innovation.'}
                </h2>
                <p className={`${isSpooky ? 'text-gray-500' : 'text-gray-600'} text-lg leading-relaxed`}>
                  {isSpooky 
                   ? "At the heart of DarkLedger is a chimera of technologies driving decisions across the full payroll lifecycle."
                   : "DarkLedger eliminates technical debt by utilizing the best tool for each layer of the financial stack."}
                </p>
            </div>
            <div className="flex justify-start md:justify-end">
                <button className={`flex items-center gap-2 px-6 py-3 rounded-full border transition-colors text-sm font-medium shadow-sm ${isSpooky ? 'bg-spooky-card border-red-900/30 text-gray-300 hover:bg-red-950' : 'bg-white border-gray-200 hover:bg-gray-50'}`}>
                    Explore <ChevronRight size={16} />
                </button>
            </div>
        </div>
        
        {/* Abstract Infrastructure Visual */}
        <div className="relative w-full h-[400px] flex items-center justify-center">
            {/* Connecting Lines */}
            <div className={`absolute w-[85%] h-[2px] top-1/2 -translate-y-1/2 z-0 hidden md:block ${isSpooky ? 'bg-red-900/20' : 'bg-gradient-to-r from-transparent via-gray-300 to-transparent'}`}></div>
            
            {/* Nodes */}
            <div className="relative z-10 w-full flex flex-col md:flex-row justify-between items-center gap-8 md:gap-0 h-full max-w-5xl mx-auto">
                
                <div className={`px-8 py-4 rounded-full font-medium shadow-lg border z-10 hover:scale-105 transition-transform ${isSpooky ? 'bg-spooky-card border-red-900/40 text-gray-400' : 'bg-white border-gray-100 text-gray-700'}`}>
                  {isSpooky ? 'The Brain (COBOL)' : 'The Calculation Layer (COBOL)'}
                </div>
                
                <div className="flex flex-col items-center gap-12">
                     <div className={`px-6 py-2 rounded-full font-medium shadow border text-sm ${isSpooky ? 'bg-spooky-card border-red-900/40 text-gray-400' : 'bg-white border-gray-100 text-gray-700'}`}>
                       {isSpooky ? 'The Body (Python)' : 'The Orchestration Layer (Python)'}
                     </div>
                     
                     {/* Center Graphic - Volcano/Engine Style */}
                     <div className={`w-72 h-48 rounded-[3rem] flex items-center justify-center text-white shadow-2xl relative overflow-hidden border-4 ring-1 ${
                        isSpooky 
                          ? 'bg-gradient-to-br from-red-700 via-black to-gray-900 shadow-red-900/30 border-gray-900 ring-red-900/50' 
                          : 'bg-gradient-to-br from-orange-400 via-orange-600 to-purple-900 shadow-orange-900/20 border-white ring-gray-100'
                     }`}>
                        <div className={`absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-20 ${isSpooky ? 'animate-pulse' : 'animate-pulse-slow'}`}></div>
                        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                        {isSpooky && <div className="absolute inset-0 flex items-center justify-center opacity-20"><Skull size={100} /></div>}
                        <span className={`text-3xl font-bold z-10 tracking-tight ${isSpooky ? 'font-spooky text-red-500 drop-shadow-md' : ''}`}>
                          {isSpooky ? 'Chimera Engine' : 'Core Logic'}
                        </span>
                     </div>
                </div>

                <div className={`px-8 py-4 rounded-full font-medium shadow-lg border z-10 hover:scale-105 transition-transform ${isSpooky ? 'bg-spooky-card border-red-900/40 text-gray-400' : 'bg-white border-gray-100 text-gray-700'}`}>
                  {isSpooky ? 'The Hands' : 'The Settlement Layer (Base)'}
                </div>

            </div>
        </div>

      </div>
    </section>
  );
};

/* --- Refined Mocks with Realistic Animation --- */

const OnboardingTerminal = () => {
  const { isSpooky } = useTheme();
  const [activeItem, setActiveItem] = useState(3); 
  const [animState, setAnimState] = useState(0); 

  useEffect(() => {
    let mounted = true;
    const loop = async () => {
        const wait = (ms: number) => new Promise(r => setTimeout(r, ms));
        while(mounted) {
            setAnimState(0); setActiveItem(3); await wait(2000);
            if (!mounted) break;
            setAnimState(1); await wait(1000);
            if (!mounted) break;
            setAnimState(2); await wait(300);
            if (!mounted) break;
            setAnimState(3); await wait(2000);
            if (!mounted) break;
            setAnimState(4); await wait(2000);
            if (!mounted) break;
            setAnimState(0); await wait(500);
        }
    };
    loop();
    return () => { mounted = false; };
  }, []);

  const getCursorStyle = () => {
      const baseX = 200, baseY = 300, targetY = 60 + (3 * 64) + 28, targetX = 260; 
      let x = baseX, y = baseY, scale = 1;
      if (animState === 0) { x = 320; y = 450; } 
      else if (animState === 1 || animState === 3 || animState === 4) { x = targetX; y = targetY; } 
      else if (animState === 2) { x = targetX; y = targetY; scale = 0.85; }
      return { transform: `translate(${x}px, ${y}px) scale(${scale})`, opacity: 1 };
  };

  const steps = [
      { icon: <Wallet size={16}/>, label: "Bank account" },
      { icon: <Layers size={16}/>, label: "Ownership structure" },
      { icon: <FileCheck size={16}/>, label: "Source of funds" },
      { icon: <Fingerprint size={16}/>, label: "Identity verification" },
      { icon: <Users size={16}/>, label: "Representatives" },
      { icon: <Building2 size={16}/>, label: "UBO" },
      { icon: <Search size={16}/>, label: "AML Screening" },
  ];

  return (
    <div className={`relative rounded-xl shadow-lg border p-6 w-[340px] select-none overflow-hidden h-[540px] transition-colors ${isSpooky ? 'bg-[#050505] border-red-900/30' : 'bg-[#FAFAFA] border-gray-200'}`}>
        <div className="absolute top-0 left-0 z-50 pointer-events-none transition-transform duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]" style={getCursorStyle()}>
            <svg width="24" height="32" viewBox="0 0 24 32" fill="none" className="drop-shadow-lg">
                <path d="M5.65376 1.83844C5.00693 1.34674 4 1.77387 4 2.5878V26.2942C4 27.2346 5.17604 27.6644 5.79815 26.951L10.9856 22.1856C11.1983 21.9902 11.4746 21.8974 11.7588 21.926L21.3197 22.8837C22.1843 22.9704 22.7562 21.9213 22.2155 21.2405L6.96348 2.04018C6.61908 1.60657 5.95995 1.49257 5.48514 1.7925L5.65376 1.83844Z" fill={isSpooky ? "#DC143C" : "black"}/>
                <path d="M6.96348 2.04018L22.2155 21.2405C22.7562 21.9213 22.1843 22.9704 21.3197 22.8837L11.7588 21.926C11.4746 21.8974 11.1983 21.9902 10.9856 22.1856L5.79815 26.951C5.17604 27.6644 4 27.2346 4 26.2942V2.5878C4 1.77387 5.00693 1.34674 5.65376 1.83844C6.12857 1.5385 6.7877 1.65251 7.1321 2.08612L6.96348 2.04018Z" stroke="white" strokeWidth="2" strokeLinejoin="round"/>
            </svg>
        </div>

        <div className="flex flex-col gap-3">
            {steps.map((step, idx) => {
                const isActive = idx === 3; 
                const isCompleted = idx < 3;
                let status = isCompleted ? 'done' : 'waiting';
                if (isActive) {
                    if (animState < 4) status = 'processing';
                    if (animState === 4) status = 'done';
                }

                const rowClass = isSpooky 
                    ? (status === 'processing' ? 'bg-[#1f0a0a] border-red-900 scale-[1.02]' : status === 'done' ? 'bg-[#0f0505] border-red-900/20 opacity-60' : 'bg-[#0f0505] border-transparent opacity-40')
                    : (status === 'processing' ? 'bg-white border-purple-200 shadow-md scale-[1.02]' : status === 'done' ? 'bg-white border-gray-100 opacity-60' : 'bg-white border-gray-100 opacity-40');

                const iconClass = isSpooky
                    ? (status === 'processing' ? 'bg-red-900 text-white' : status === 'done' ? 'bg-red-900/30 text-red-500' : 'bg-gray-900 text-gray-600')
                    : (status === 'processing' ? 'bg-[#6366f1] text-white' : status === 'done' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400');

                const textClass = isSpooky
                    ? (status === 'processing' ? 'text-gray-200' : 'text-gray-600')
                    : (status === 'processing' ? 'text-gray-900' : 'text-gray-500');

                return (
                    <div key={idx} className={`group relative flex items-center gap-4 p-3 rounded-lg border transition-all duration-300 ${rowClass}`}>
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${iconClass}`}>
                            {step.icon}
                        </div>
                        <div className="flex-1">
                            <div className={`text-sm font-semibold ${textClass}`}>
                                {step.label}
                            </div>
                        </div>
                        <div>
                            {status === 'done' && <CheckCircle size={18} className={isSpooky ? "text-red-600" : "text-green-500"} />}
                            {status === 'processing' && (
                                <div className={`w-4 h-4 border-2 border-t-transparent rounded-full animate-spin ${isSpooky ? 'border-red-600' : 'border-purple-500'}`}></div>
                            )}
                        </div>
                    </div>
                )
            })}
        </div>
    </div>
  );
}

const DecideMockup = () => {
    const { isSpooky } = useTheme();
    const [toggled, setToggled] = useState(false);
    const [animPhase, setAnimPhase] = useState(0); 

    useEffect(() => {
        let mounted = true;
        const loop = async () => {
            const wait = (ms: number) => new Promise(r => setTimeout(r, ms));
            while(mounted) {
                setAnimPhase(0); setToggled(false); await wait(2000);
                if (!mounted) break;
                setAnimPhase(1); await wait(1000);
                if (!mounted) break;
                setAnimPhase(2); await wait(200); setToggled(true);
                if (!mounted) break;
                setAnimPhase(3); await wait(3000);
            }
        }
        loop();
        return () => { mounted = false; };
    }, []);

    const getCursorStyle = () => {
        let x = 300, y = 400, scale = 1, targetX = 260, targetY = 220;
        if (animPhase === 0) { x = 350; y = 450; }
        else if (animPhase === 1 || animPhase === 3) { x = targetX; y = targetY; }
        else if (animPhase === 2) { x = targetX; y = targetY; scale = 0.85; }
        return { transform: `translate(${x}px, ${y}px) scale(${scale})`, opacity: 1 };
    };

    const cardClass = (opacity: string, translateZ: string, scale: string) => {
        const base = isSpooky ? 'bg-[#0f0505] border-red-900/30 shadow-black' : 'bg-white border-gray-100 shadow-lg';
        return `absolute left-0 w-full rounded-xl shadow-xl border p-5 transform ${opacity} ${translateZ} ${scale} ${base}`;
    }

    return (
        <div className="relative w-full h-[500px] flex items-center justify-center overflow-hidden">
             <div className="absolute top-0 left-0 z-50 pointer-events-none transition-transform duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]" style={getCursorStyle()}>
                <svg width="24" height="32" viewBox="0 0 24 32" fill="none" className="drop-shadow-xl">
                    <path d="M5.65376 1.83844C5.00693 1.34674 4 1.77387 4 2.5878V26.2942C4 27.2346 5.17604 27.6644 5.79815 26.951L10.9856 22.1856C11.1983 21.9902 11.4746 21.8974 11.7588 21.926L21.3197 22.8837C22.1843 22.9704 22.7562 21.9213 22.2155 21.2405L6.96348 2.04018C6.61908 1.60657 5.95995 1.49257 5.48514 1.7925L5.65376 1.83844Z" fill={isSpooky ? "#DC143C" : "black"}/>
                    <path d="M6.96348 2.04018L22.2155 21.2405C22.7562 21.9213 22.1843 22.9704 21.3197 22.8837L11.7588 21.926C11.4746 21.8974 11.1983 21.9902 10.9856 22.1856L5.79815 26.951C5.17604 27.6644 4 27.2346 4 26.2942V2.5878C4 1.77387 5.00693 1.34674 5.65376 1.83844C6.12857 1.5385 6.7877 1.65251 7.1321 2.08612L6.96348 2.04018Z" stroke="white" strokeWidth="2" strokeLinejoin="round"/>
                </svg>
            </div>

            <div className="relative w-[320px] h-[380px] perspective-1000 transform scale-90 md:scale-100">
                <div className={`relative w-full h-full transform preserve-3d rotate-x-6 rotate-y-[-12deg] rotate-z-2 ${isSpooky ? 'animate-float-ghost' : 'animate-[pulse_6s_infinite]'}`}>
                    
                    {/* Bottom Card */}
                    <div className={`${cardClass('opacity-40', 'translate-z-[-40px]', 'scale-95')} top-[60px]`}>
                        <div className={`h-2 w-1/3 rounded mb-4 ${isSpooky ? 'bg-gray-800' : 'bg-gray-200'}`}></div>
                        <div className="space-y-3">
                            <div className={`h-8 w-full rounded border ${isSpooky ? 'bg-gray-900 border-gray-800' : 'bg-gray-50 border-gray-100'}`}></div>
                            <div className={`h-8 w-full rounded border ${isSpooky ? 'bg-gray-900 border-gray-800' : 'bg-gray-50 border-gray-100'}`}></div>
                        </div>
                    </div>

                     {/* Middle Card */}
                     <div className={`${cardClass('opacity-70', 'translate-z-[-20px]', 'scale-[0.97]')} top-[30px]`}>
                        <div className={`h-2 w-1/3 rounded mb-4 ${isSpooky ? 'bg-gray-800' : 'bg-gray-200'}`}></div>
                        <div className="space-y-3">
                             <div className={`flex items-center justify-between p-2 rounded border ${isSpooky ? 'bg-gray-900 border-gray-800' : 'bg-gray-50 border-gray-100'}`}>
                                <span className="text-xs text-gray-500">Ownership</span>
                             </div>
                        </div>
                    </div>

                    {/* Top Card */}
                    <div className={`absolute top-0 left-0 w-full rounded-xl shadow-2xl border p-6 transform translate-z-0 transition-all hover:translate-y-[-5px] ${isSpooky ? 'bg-[#0a0a0a] border-red-900/50 shadow-red-900/10' : 'bg-white border-gray-200'}`}>
                        <div className="flex items-center gap-3 mb-6">
                            <div className={`p-2 rounded-lg ${isSpooky ? 'bg-red-900/30 text-red-500' : 'bg-blue-50 text-blue-500'}`}>
                                <Shield size={20} />
                            </div>
                            <div>
                                <h3 className={`text-sm font-bold leading-tight ${isSpooky ? 'text-gray-200' : 'text-gray-900'}`}>
                                    {isSpooky ? 'Suspected Curse Hit' : 'Compliance Check'}
                                </h3>
                                <p className="text-[10px] text-gray-500 font-medium uppercase tracking-wider mt-0.5">High Priority</p>
                            </div>
                        </div>

                        <div className="space-y-3">
                            <div className={`flex items-center justify-between p-3 border rounded-lg shadow-sm ${isSpooky ? 'bg-black border-gray-800' : 'bg-white border-gray-100'}`}>
                                <span className="text-sm font-medium text-gray-500">Geographic activity</span>
                                <div className="w-4 h-4 rounded-full border-2 border-gray-600"></div>
                            </div>
                            
                            <div className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-300 ${toggled ? (isSpooky ? 'bg-red-900/20 border-red-900' : 'bg-[#dbeafe] border-blue-200') : (isSpooky ? 'bg-black border-gray-800' : 'bg-white border-gray-100 shadow-sm')}`}>
                                <span className={`text-sm font-medium transition-colors ${toggled ? (isSpooky ? 'text-red-400' : 'text-blue-700') : 'text-gray-500'}`}>
                                    {isSpooky ? 'Source of souls' : 'Source of funds'}
                                </span>
                                <div className={`w-10 h-6 rounded-full p-1 transition-colors ${toggled ? (isSpooky ? 'bg-red-700' : 'bg-blue-600') : (isSpooky ? 'bg-gray-800' : 'bg-gray-200')}`}>
                                    <div className={`w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform ${toggled ? 'translate-x-4' : 'translate-x-0'}`}></div>
                                </div>
                            </div>

                            <div className={`flex items-center justify-between p-3 border rounded-lg shadow-sm opacity-60 ${isSpooky ? 'bg-black border-gray-800' : 'bg-white border-gray-100'}`}>
                                <span className="text-sm font-medium text-gray-500">Ownership structure</span>
                                <div className="w-4 h-4 rounded-full border-2 border-gray-600"></div>
                            </div>
                        </div>

                        <div className={`mt-6 pt-4 border-t flex gap-2 ${isSpooky ? 'border-gray-800' : 'border-gray-50'}`}>
                             <div className={`h-2 w-full rounded-full overflow-hidden ${isSpooky ? 'bg-gray-900' : 'bg-gray-100'}`}>
                                 <div className={`h-full w-2/3 ${isSpooky ? 'bg-red-700' : 'bg-blue-500'}`}></div>
                             </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}

const FeatureSection = ({ 
  tag, title, desc, align = 'left', features, mockContent 
}: { 
  tag: string, title: string, desc: string, align?: 'left' | 'right', features?: string[], mockContent: React.ReactNode 
}) => {
  const { isSpooky } = useTheme();

  return (
    <section className={`py-24 border-b last:border-0 transition-colors duration-500 ${isSpooky ? 'bg-black border-gray-900 odd:bg-[#050505]' : 'bg-[#FAFAFA] odd:bg-white border-gray-100'}`}>
      <div className="max-w-7xl mx-auto px-6">
        <div className={`flex flex-col ${align === 'right' ? 'md:flex-row-reverse' : 'md:flex-row'} gap-16 items-center`}>
          
          <div className="flex-1 space-y-8">
            <span className={`inline-block px-3 py-1 rounded-full border text-xs font-bold uppercase tracking-wider shadow-sm ${isSpooky ? 'bg-red-900/20 border-red-900/50 text-red-400' : 'bg-white border-gray-200 text-gray-600'}`}>
                {tag}
            </span>
            <div className="space-y-4">
                 <h2 className={`text-4xl md:text-5xl font-semibold tracking-tighter ${isSpooky ? 'text-spooky-accent font-spooky' : 'text-duna-900'}`}>{title}</h2>
                 <p className={`text-lg leading-relaxed max-w-lg font-normal ${isSpooky ? 'text-gray-500' : 'text-gray-600'}`}>{desc}</p>
            </div>
            
            {features && features.length > 0 && (
               <div className="space-y-5 pt-4">
                  {features.map((f, i) => (
                      <div key={i} className="flex gap-4 group">
                           <div className={`mt-1 transition-colors ${isSpooky ? 'text-gray-700 group-hover:text-red-600' : 'text-gray-300 group-hover:text-black'}`}><CheckCircle size={20}/></div>
                           <div>
                               <h4 className={`font-semibold ${isSpooky ? 'text-gray-300' : 'text-gray-900'}`}>{f.split(':')[0]}</h4>
                               <p className={`text-sm mt-1 ${isSpooky ? 'text-gray-600' : 'text-gray-500'}`}>{f.split(':')[1]}</p>
                           </div>
                      </div>
                  ))}
               </div>
            )}
             <div className="hidden md:flex pt-4">
                 <button className={`flex items-center gap-2 text-sm font-bold border-b pb-0.5 hover:gap-3 transition-all ${isSpooky ? 'text-spooky-accent border-spooky-accent' : 'text-black border-black'}`}>Explore <ArrowRight size={16}/></button>
             </div>
          </div>

          {/* Graphic Side */}
          <div className="flex-1 w-full flex justify-center">
            <div className={`rounded-[2rem] p-8 md:p-12 w-full min-h-[600px] flex items-center justify-center relative overflow-hidden ${isSpooky ? 'bg-[#0a0505]/80' : 'bg-sand/40'}`}>
                <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] opacity-5"></div>
                {mockContent}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

const Security = () => {
    const { isSpooky } = useTheme();
    return (
        <section className={`py-32 border-y transition-colors duration-500 ${isSpooky ? 'bg-black border-red-900/20' : 'bg-sand/30 border-sand-dark/50'}`}>
            <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-end justify-between gap-12">
                <div className="max-w-2xl">
                    <h2 className={`text-4xl font-semibold tracking-tighter mb-6 ${isSpooky ? 'text-spooky-accent font-spooky' : 'text-duna-900'}`}>
                        {isSpooky ? 'Safe and Secure (Mostly)' : 'Compliance via Code.'}
                    </h2>
                    <p className={`${isSpooky ? 'text-gray-500' : 'text-gray-600'} text-lg leading-relaxed`}>
                        {isSpooky 
                         ? "Your data is our obsession. DarkLedger is designed with a deep commitment to Byte-Perfect Integrity. We don't just \"process\" data; we etch it into the binary void."
                         : "DarkLedger is designed with a \"Safety First\" architecture. We segregate calculation logic from network logic to prevent attack vectors."}
                    </p>
                    <button className={`mt-8 px-6 py-3 rounded-full border text-sm font-medium hover:shadow-md transition-all flex items-center gap-2 ${isSpooky ? 'bg-red-900/10 border-red-900 text-red-500' : 'bg-white border-gray-300'}`}>
                        Explore <ChevronRight size={16} />
                    </button>
                </div>
                <div className={`flex gap-6 opacity-60 grayscale hover:grayscale-0 transition-all duration-500 ${isSpooky ? 'invert brightness-50' : ''}`}>
                    <div className="bg-white border border-gray-200 rounded-full w-24 h-24 flex flex-col items-center justify-center p-2 text-center text-[10px] font-bold leading-tight shadow-sm">
                        {isSpooky ? 'COBOL 85\nCompliant' : 'SOC 2\nType II'}
                    </div>
                    <div className="bg-white border border-gray-200 rounded-full w-24 h-24 flex flex-col items-center justify-center p-2 text-center text-[10px] font-bold leading-tight shadow-sm">
                        {isSpooky ? 'SOC 2\nPending' : 'ISO 27001\nCompliant'}
                    </div>
                    <div className="bg-white border border-gray-200 rounded-full w-24 h-24 flex flex-col items-center justify-center p-2 text-center text-[10px] font-bold leading-tight shadow-sm">
                        {isSpooky ? 'ISO 27001\nGraveyard' : 'GnuCOBOL\nVerified'}
                    </div>
                </div>
            </div>
        </section>
    )
}

const News = () => {
    const { isSpooky } = useTheme();
    const articles = isSpooky ? [
        {
            title: "Why we chose COBOL in 2025",
            meta: "Tech Blog — 6 min read",
            image: "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2940&auto=format&fit=crop" // tech chip
        },
        {
            title: "The danger of Floating Point Arithmetic",
            meta: "Engineering — 19 min watch",
            image: "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?q=80&w=2874&auto=format&fit=crop" // code screen
        },
        {
            title: "Summoning the Daemon: A DevOps Guide",
            meta: "Guides — 13 min read",
            image: "https://images.unsplash.com/photo-1505664194779-8beaceb93744?q=80&w=2940&auto=format&fit=crop" // dark room
        }
    ] : [
        {
            title: "The Hidden Cost of Floating Point Errors in Fintech",
            meta: "Whitepaper — 15 min read",
            image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2940&auto=format&fit=crop"
        },
        {
            title: "Why COBOL is still the bedrock of Global Finance",
            meta: "Blog — 8 min read",
            image: "https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2940&auto=format&fit=crop"
        },
        {
            title: "Base L2: The Future of Payroll Settlement",
            meta: "Insights — 12 min read",
            image: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=2832&auto=format&fit=crop"
        }
    ];

    return (
        <section className={`py-24 transition-colors duration-500 ${isSpooky ? 'bg-black' : 'bg-[#FAFAFA]'}`}>
            <div className="max-w-7xl mx-auto px-6">
                <div className="flex justify-between items-end mb-12">
                    <h2 className={`text-4xl font-semibold tracking-tighter ${isSpooky ? 'text-spooky-accent font-spooky' : 'text-duna-900'}`}>
                        {isSpooky ? 'News from the Crypt' : 'Industry Insights'}
                    </h2>
                    <a href="#" className={`text-sm font-medium border-b pb-0.5 transition-colors ${isSpooky ? 'text-gray-500 border-gray-700 hover:text-white' : 'text-black border-gray-300 hover:border-black'}`}>See more</a>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                    {articles.map((article, idx) => (
                        <div key={idx} className="group cursor-pointer">
                            <div className={`aspect-[4/3] rounded-2xl overflow-hidden mb-6 shadow-sm relative ${isSpooky ? 'bg-gray-900' : 'bg-gray-200'}`}>
                                <img src={article.image} alt={article.title} className={`w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out ${isSpooky ? 'opacity-50 grayscale' : ''}`} />
                                <div className="absolute inset-0 bg-black/5 group-hover:bg-transparent transition-colors"></div>
                            </div>
                            <h3 className={`text-xl font-semibold mb-3 transition-colors tracking-tight leading-snug ${isSpooky ? 'text-gray-400 group-hover:text-red-500' : 'text-black group-hover:text-gray-600'}`}>{article.title}</h3>
                            <p className="text-xs text-gray-500 font-bold uppercase tracking-wider">{article.meta}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    )
}

const TrafficStats = () => {
    const { isSpooky } = useTheme();
    const [view, setView] = useState('monthly');

    const data = useMemo(() => {
        if (view === 'daily') {
             return Array.from({ length: 14 }).map((_, i) => ({
                 name: `Day ${i + 1}`,
                 visitors: Math.floor(Math.random() * 500) + 1000 + (i * 50)
             }));
        } else if (view === 'weekly') {
             return Array.from({ length: 8 }).map((_, i) => ({
                 name: `Wk ${i + 1}`,
                 visitors: Math.floor(Math.random() * 2000) + 5000 + (i * 200)
             }));
        } else {
             return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].map((m, i) => ({
                 name: m,
                 visitors: Math.floor(Math.random() * 10000) + 20000 + (i * 1000)
             }));
        }
    }, [view]);

    return (
        <section className={`py-24 transition-colors duration-500 ${isSpooky ? 'bg-black' : 'bg-[#FAFAFA]'}`}>
             <div className="max-w-7xl mx-auto px-6">
                <FadeIn>
                    <div className="flex flex-col md:flex-row justify-between items-end mb-12 gap-6">
                        <div>
                            <h2 className={`text-4xl font-semibold tracking-tighter mb-4 ${isSpooky ? 'text-spooky-accent font-spooky' : 'text-duna-900'}`}>
                                {isSpooky ? 'Soul Harvesting Trends' : 'Platform Traffic Trends'}
                            </h2>
                            <p className={`${isSpooky ? 'text-gray-500' : 'text-gray-600'} max-w-xl`}>
                                {isSpooky ? 'Track the influx of fresh souls entering the crypt.' : 'Visualize growth and engagement metrics over time.'}
                            </p>
                        </div>
                        <div className={`flex p-1 rounded-lg border ${isSpooky ? 'bg-gray-900 border-gray-800' : 'bg-white border-gray-200'}`}>
                            {['daily', 'weekly', 'monthly'].map((v) => (
                                <button 
                                    key={v}
                                    onClick={() => setView(v)}
                                    className={`px-4 py-2 rounded-md text-sm font-medium transition-all capitalize ${
                                        view === v 
                                        ? (isSpooky ? 'bg-red-900 text-white shadow-sm' : 'bg-gray-900 text-white shadow-sm')
                                        : (isSpooky ? 'text-gray-400 hover:text-white' : 'text-gray-500 hover:text-black')
                                    }`}
                                >
                                    {v}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className={`w-full h-[400px] rounded-2xl border p-6 shadow-sm transition-colors duration-500 ${isSpooky ? 'bg-[#0f0505] border-red-900/20' : 'bg-white border-gray-100'}`}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data}>
                                <defs>
                                    <linearGradient id="colorVisitors" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor={isSpooky ? '#DC143C' : '#111'} stopOpacity={0.1}/>
                                        <stop offset="95%" stopColor={isSpooky ? '#DC143C' : '#111'} stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke={isSpooky ? '#333' : '#f3f4f6'} vertical={false} />
                                <XAxis 
                                    dataKey="name" 
                                    axisLine={false} 
                                    tickLine={false} 
                                    tick={{ fill: isSpooky ? '#666' : '#9ca3af', fontSize: 12 }} 
                                    dy={10}
                                />
                                <YAxis 
                                    axisLine={false} 
                                    tickLine={false} 
                                    tick={{ fill: isSpooky ? '#666' : '#9ca3af', fontSize: 12 }}
                                    tickFormatter={(value) => `${value / 1000}k`} 
                                />
                                <Tooltip 
                                    contentStyle={{ 
                                        backgroundColor: isSpooky ? '#000' : '#fff', 
                                        borderColor: isSpooky ? '#333' : '#e5e7eb',
                                        borderRadius: '8px',
                                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                                        color: isSpooky ? '#fff' : '#000'
                                    }}
                                    itemStyle={{ color: isSpooky ? '#DC143C' : '#111' }}
                                />
                                <Area 
                                    type="monotone" 
                                    dataKey="visitors" 
                                    stroke={isSpooky ? '#DC143C' : '#111'} 
                                    strokeWidth={2}
                                    fillOpacity={1} 
                                    fill="url(#colorVisitors)" 
                                    animationDuration={1000}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </FadeIn>
             </div>
        </section>
    )
}

const Footer = () => {
    const { isSpooky } = useTheme();

    return (
        <footer className={`relative py-20 overflow-hidden font-sans transition-colors duration-500 ${isSpooky ? 'bg-black text-gray-400' : 'bg-[#111] text-gray-400'}`}>
            
            {/* --- Background Elements --- */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none">
                 <img 
                    src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2940&auto=format&fit=crop" 
                    alt="Background" 
                    className={`w-full h-full object-cover object-center grayscale mix-blend-overlay ${isSpooky ? 'invert contrast-150' : ''}`}
                />
                 <div className={`absolute inset-0 bg-gradient-to-t ${isSpooky ? 'from-black via-red-950/20 to-transparent' : 'from-[#111] via-[#111]/80 to-transparent'}`}></div>
            </div>

            <div className="relative z-10 max-w-7xl mx-auto px-6">
                
                {/* --- Top Section: Brand & Newsletter --- */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 border-b border-white/10 pb-12 mb-12">
                    {/* Brand Column */}
                    <div className="lg:col-span-5 space-y-6">
                        {/* Modified Brand Header with Logo */}
                        <div className="flex items-center gap-4">
                            <DarkLedgerLogo 
                                className={`w-12 h-12 transition-all duration-500 ${isSpooky ? 'brightness-125 sepia-[.5] hue-rotate-[-50deg] drop-shadow-[0_0_8px_rgba(220,38,38,0.6)]' : ''}`} 
                            />
                            <span className={`text-3xl font-bold tracking-tighter ${isSpooky ? 'text-red-600 font-spooky animate-pulse' : 'text-white'}`}>
                                DARKLEDGER
                            </span>
                        </div>

                        <p className="text-sm leading-relaxed opacity-80 max-w-sm">
                            {isSpooky 
                                ? "We stitch the fabric of modern finance with the cursed threads of legacy code. Precision in every byte, horror in every bit." 
                                : "Bridging the gap between mainframe reliability and blockchain agility. The only payroll infrastructure you will ever need."}
                        </p>
                        
                        {/* System Status Indicator */}
                        <div className="flex items-center gap-3 text-xs font-mono border border-white/10 w-fit px-3 py-1.5 rounded-full bg-white/5">
                            <span className={`relative flex h-2 w-2`}>
                              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isSpooky ? 'bg-red-500' : 'bg-emerald-400'}`}></span>
                              <span className={`relative inline-flex rounded-full h-2 w-2 ${isSpooky ? 'bg-red-600' : 'bg-emerald-500'}`}></span>
                            </span>
                            <span className={isSpooky ? 'text-red-400' : 'text-emerald-400'}>
                                {isSpooky ? 'SYSTEM HAUNTED' : 'ALL SYSTEMS OPERATIONAL'}
                            </span>
                        </div>
                    </div>

                    {/* Newsletter Column */}
                    <div className="lg:col-span-7 flex flex-col justify-center lg:items-end">
                         <div className="w-full max-w-md">
                            <h4 className={`text-sm font-bold uppercase tracking-widest mb-4 ${isSpooky ? 'text-red-500' : 'text-white'}`}>
                                {isSpooky ? 'Summon Updates' : 'Subscribe to Newsletter'}
                            </h4>
                            <div className="flex gap-2">
                                <input 
                                    type="email" 
                                    placeholder="enter_your_email_address..." 
                                    className={`w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-1 transition-all
                                    ${isSpooky ? 'focus:ring-red-900 focus:border-red-900 text-red-100 placeholder:text-red-900/50' : 'focus:ring-white focus:border-white text-white placeholder:text-gray-600'}`}
                                />
                                <button className={`px-6 py-3 rounded-lg font-bold text-sm flex items-center gap-2 transition-all group
                                    ${isSpooky ? 'bg-red-900 text-white hover:bg-red-800' : 'bg-white text-black hover:bg-gray-200'}`}>
                                    <span>Join</span>
                                    <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                                </button>
                            </div>
                         </div>
                    </div>
                </div>

                {/* --- Middle Section: Links Grid --- */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-20">
                    {[
                        { title: "Platform", links: ["Calculation Engine", "Settlement Layer", "Compliance", "API Docs"] },
                        { title: "Company", links: ["About Us", "Careers", "The Team", "Contact"] },
                        { title: "Resources", links: ["Blog", "Case Studies", "Whitepaper", "Support"] },
                        { title: "Legal", links: ["Privacy Policy", "Terms of Service", "Cookie Policy", "Security"] }
                    ].map((col, idx) => (
                        <div key={idx} className="space-y-6">
                            <h4 className={`font-bold text-xs uppercase tracking-widest ${isSpooky ? 'text-gray-500' : 'text-gray-200'}`}>
                                {col.title}
                            </h4>
                            <ul className="space-y-3 text-sm">
                                {col.links.map((link, lIdx) => (
                                    <li key={lIdx}>
                                        <a href="#" className={`transition-colors duration-200 flex items-center gap-2 group
                                            ${isSpooky ? 'hover:text-red-500 hover:tracking-widest' : 'hover:text-white'}`}>
                                            {isSpooky && <span className="w-1 h-1 bg-red-800 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"></span>}
                                            {link}
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
                
                {/* --- Bottom Section: Copyright & Socials --- */}
                <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-6">
                    <p className="text-xs font-medium opacity-50">
                        {isSpooky 
                            ? '© 2025 DarkLedger Inc. Void warranties included.' 
                            : '© 2025 DarkLedger Inc. Precision in every byte.'}
                    </p>

                    <div className="flex gap-6">
                        {[Github, Twitter, Linkedin].map((Icon, i) => (
                            <a key={i} href="#" className={`transition-transform hover:-translate-y-1 ${isSpooky ? 'hover:text-red-500' : 'hover:text-white'}`}>
                                <Icon size={20} />
                            </a>
                        ))}
                    </div>
                </div>
            </div>
        </footer>
    )
}

/* --- App Content Wrapper to consume Theme --- */

const AppContent = () => {
    const { isSpooky } = useTheme();

    const lifecycleMockup = (
      <div className={`w-[85%] rounded-2xl shadow-2xl overflow-hidden border ${isSpooky ? 'bg-[#0f0505] border-red-900/30' : 'bg-white border-gray-100'}`}>
          <div className={`p-4 border-b flex justify-between items-center ${isSpooky ? 'bg-black border-gray-800' : 'bg-gray-50/50 border-gray-100'}`}>
              <div className="flex gap-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-red-800"></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-gray-600"></div>
                  <div className="w-2.5 h-2.5 rounded-full bg-gray-800"></div>
              </div>
          </div>
          <div className="p-6 space-y-4">
              <div className={`flex items-start gap-4 p-4 rounded-xl cursor-default ${isSpooky ? 'bg-black hover:bg-gray-900' : 'bg-gray-50 hover:bg-gray-100'}`}>
                  <div className={`p-2 rounded-lg shadow-sm ${isSpooky ? 'bg-gray-900' : 'bg-white'}`}>
                    <RefreshCw size={18} className="text-gray-500"/>
                  </div>
                  <div>
                      <div className={`text-sm font-bold ${isSpooky ? 'text-gray-300' : 'text-gray-800'}`}>
                        {isSpooky ? 'PEP' : 'Daily Re-Sync'}
                      </div>
                      <div className="text-xs text-gray-600 mt-0.5 font-medium">Updated 2 hours ago</div>
                  </div>
              </div>
               <div className={`flex items-start gap-4 p-4 border shadow-lg rounded-xl transform scale-105 z-10 ${isSpooky ? 'bg-[#1a0505] border-red-900/60' : 'bg-white border-gray-200'}`}>
                  <div className={`p-2 rounded-lg ${isSpooky ? 'bg-red-900/30' : 'bg-green-50'}`}>
                    <Activity size={18} className={`${isSpooky ? 'text-red-600' : 'text-green-600'}`}/>
                  </div>
                  <div>
                      <div className={`text-sm font-bold ${isSpooky ? 'text-white' : 'text-gray-800'}`}>
                        {isSpooky ? 'Adverse media' : 'USDC Settlement'}
                      </div>
                      <div className="text-xs text-gray-500 mt-0.5 font-medium">Confirmed on-chain</div>
                  </div>
              </div>
               <div className={`flex items-start gap-4 p-4 rounded-xl cursor-default ${isSpooky ? 'bg-black hover:bg-gray-900' : 'bg-gray-50 hover:bg-gray-100'}`}>
                  <div className={`p-2 rounded-lg shadow-sm ${isSpooky ? 'bg-gray-900' : 'bg-white'}`}>
                    <Shield size={18} className="text-gray-500"/>
                  </div>
                  <div>
                      <div className={`text-sm font-bold ${isSpooky ? 'text-gray-300' : 'text-gray-800'}`}>
                        {isSpooky ? 'Sanctions' : 'Tax Reserve'}
                      </div>
                      <div className="text-xs text-gray-600 mt-0.5 font-medium">Locked in Vault</div>
                  </div>
              </div>
          </div>
      </div>
  )

    return (
        <div className={`min-h-screen font-sans selection:bg-red-900 selection:text-white transition-colors duration-500 ${isSpooky ? 'bg-black text-gray-300' : 'bg-[#FAFAFA] text-gray-900'}`}>
            <Navbar />
            <Hero />
            <Stats />
            <ValueProps />
            <Testimonials />
            <Infrastructure />
            
            <div id="features" className="flex flex-col">
                <FeatureSection 
                    tag={isSpooky ? "The Brain" : "The Calculation Layer"}
                    title={isSpooky ? "64-Bit Fixed-Point Accuracy" : "Zero-Error Arithmetic"}
                    desc={isSpooky 
                        ? "JavaScript 0.1 + 0.2 fails. COBOL COMPUTE ROUNDED never misses. We use strict byte-level logic to ensure every cent is accounted for before it hits the chain."
                        : "Standard JavaScript math (0.1 + 0.2) often results in 0.30000000000000004. Our isolated COBOL environment uses Fixed-Point Arithmetic to ensure tax calculations are mathematically perfect before any funds move."}
                    features={isSpooky ? [] : []}
                    mockContent={<OnboardingTerminal />}
                />
                
                <FeatureSection 
                    tag={isSpooky ? "The Body" : "The Orchestration Layer"}
                    title={isSpooky ? "IPC \"Stitching\" Protocol" : "Secure Data Marshalling"}
                    desc={isSpooky 
                        ? "Our proprietary Python bridge orchestrates the subprocess communication, translating modern JSON into fixed-width mainframe records in milliseconds."
                        : "A hardened Python API manages the subprocess lifecycle, validating inputs against a strict 23-byte schema before they ever touch the calculation core."}
                    align="right"
                    features={isSpooky ? [] : []}
                    mockContent={<DecideMockup />}
                />

                <FeatureSection 
                    tag={isSpooky ? "The Hands" : "The Settlement Layer"}
                    title={isSpooky ? "Instant USDC Payouts" : "Programmatic Money"}
                    desc={isSpooky 
                        ? "Once the math is verified by the dead, the living get paid. Native USDC integration on Base means your employees get paid in seconds, globally."
                        : "Once validated, funds are dispersed via USDC on Base. This offers transparency for the employer and instant liquidity for the employee, without the volatility of standard crypto assets."}
                    features={isSpooky ? [] : []}
                    mockContent={lifecycleMockup}
                />
            </div>

            <Security />
            <News />
            <TrafficStats />
            <Footer />
        </div>
    );
};

export default function App() {
  const [isSpooky, setIsSpooky] = useState(false);

  const toggleTheme = () => setIsSpooky(!isSpooky);

  return (
      <ThemeContext.Provider value={{ isSpooky, toggleTheme }}>
          <AppContent />
      </ThemeContext.Provider>
  );
}