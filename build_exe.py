#!/usr/bin/env python
"""
Script para construir el ejecutable Windows
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean_build_folders():
    """Limpia carpetas de compilación anteriores"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"🗑️  Limpiando carpeta: {folder}")
            shutil.rmtree(folder)
    
    # Limpia archivos .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()

def build_executable():
    """Construye el ejecutable con PyInstaller"""
    print("🔨 Construyendo ejecutable Windows...")
    
    # Opciones de PyInstaller
    pyinstaller_options = [
        'pyinstaller',
        '--name=Triglyceride_Analysis_System',
        '--onefile',
        '--console', 
        '--add-data=src;src',
        '--hidden-import=matplotlib.backends.backend_tkagg',
        '--hidden-import=scipy',
        '--hidden-import=sklearn',
        '--collect-all=opencv-python',
        '--clean',
        'src/main.py'
    ]
    
    try:
        result = subprocess.run(pyinstaller_options, check=True)
        print("✅ Ejecutable construido exitosamente!")
        
        exe_path = Path('dist/Triglyceride_Analysis_System.exe')
        if exe_path.exists():
            shutil.copy(exe_path, 'Triglyceride_Analysis_System.exe')
            print(f"📦 Ejecutable disponible en: {Path().absolute()}/Triglyceride_Analysis_System.exe")
            
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📏 Tamaño del ejecutable: {size_mb:.2f} MB")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al construir el ejecutable: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller no encontrado. Instálalo con: pip install pyinstaller")
        return False
    
    return True

def create_installer():
    """Crea un instalador (opcional, requiere Inno Setup)"""
    print("\n📦 Creando instalador...")
    
    iss_content = """[Setup]
AppName=Triglyceride Analysis System
AppVersion=1.0.0
AppPublisher=IPICYT
DefaultDirName={pf}\\Triglyceride Analysis System
DefaultGroupName=Triglyceride Analysis System
OutputDir=installer
OutputBaseFilename=TriglycerideAnalysisSystem_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\Triglyceride_Analysis_System.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\\*"; DestDir: "{app}\\docs"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\\Triglyceride Analysis System"; Filename: "{app}\\Triglyceride_Analysis_System.exe"
Name: "{commondesktop}\\Triglyceride Analysis System"; Filename: "{app}\\Triglyceride_Analysis_System.exe"
"""
    
    with open('setup.iss', 'w', encoding='utf-8') as f:
        f.write(iss_content)
    
    print("📝 Script de instalación creado (setup.iss)")
    print("💡 Para crear el instalador, instala Inno Setup y compila setup.iss")

def main():
    print("="*60)
    print("   CONSTRUCTOR DE EJECUTABLE WINDOWS")
    print("="*60)
    
    clean_build_folders()
    
    if not build_executable():
        sys.exit(1)
  
    
    print("\n" + "="*60)
    print("🎉 ¡Proceso completado!")
    print("="*60)
    
    print("\n📋 PASOS PARA DISTRIBUIR:")
    print("1. El ejecutable está en: Triglyceride_Analysis_System.exe")
    print("2. Para distribuir, comprime:")
    print("   - Triglyceride_Analysis_System.exe")
    print("   - README.md")
    print("   - Carpeta 'docs/'")
    print("\n⚠️  Nota: El ejecutable puede ser grande (>50MB)")
    print("   debido a las dependencias de OpenCV y Matplotlib")

if __name__ == "__main__":
    main()
