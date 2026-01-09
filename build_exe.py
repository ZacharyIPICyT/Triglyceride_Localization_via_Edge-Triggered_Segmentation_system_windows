#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
from pathlib import Path

def print_banner():
    print("="*70)
    print("    🧪 TRIGLYCERIDE ANALYSIS SYSTEM - WINDOWS BUILDER")
    print("="*70)
    print("🔬 IPICYT - 25° Aniversario")
    print("📦 Creando ejecutable Windows (.exe)")
    print("="*70)

def clean_previous_builds():
    """Limpia compilaciones anteriores"""
    print("\n🗑️  Limpiando compilaciones anteriores...")
    
    folders_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['*.spec', '*.log']
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✓ Eliminado: {folder}")
    
    for pattern in files_to_remove:
        for file in Path('.').glob(pattern):
            file.unlink()
            print(f"  ✓ Eliminado: {file}")

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        'opencv-python',
        'numpy',
        'matplotlib',
        'pandas',
        'pyinstaller',
        'pywin32',
        'pillow',
        'scipy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_') if '-' in package else package)
            print(f"  ✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ✗ {package} (faltante)")
    
    if missing:
        print(f"\n❌ Faltan dependencias: {', '.join(missing)}")
        print("   Instala con: pip install " + " ".join(missing))
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def build_windows_executable():
    """Construye el ejecutable con PyInstaller"""
    print("\n🔨 Construyendo ejecutable Windows...")
    

    pyinstaller_cmd = [
        'pyinstaller',
        '--name=Triglyceride_Analysis_System',
        '--onefile',                    
        '--console',                
        '--icon=assets/icon.ico',    
        '--add-data=README.md;.',      
        '--hidden-import=matplotlib.backends.backend_tkagg',
        '--hidden-import=scipy',
        '--hidden-import=scipy.sparse.csgraph',
        '--hidden-import=pandas',
        '--hidden-import=pytz',
        '--hidden-import=six',
        '--hidden-import=sklearn',
        '--clean',
        '--noupx',                      
        'src/main.py'                 
    ]
    
    print("📋 Comando PyInstaller:")
    print("   " + " ".join(pyinstaller_cmd[:5]) + " \\")
    print("   " + " ".join(pyinstaller_cmd[5:10]) + " \\")
    print("   " + " ".join(pyinstaller_cmd[10:]))
    
    try:
        print("\n⏳ Compilando (esto puede tomar varios minutos)...")
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            return True
        else:
            print(f"❌ Error en compilación: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar PyInstaller: {e}")
        print(f"Salida de error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller no encontrado. Instala con: pip install pyinstaller")
        return False

def verify_executable():
    """Verifica que el ejecutable se creó correctamente"""
    print("\n🔍 Verificando ejecutable creado...")
    
    exe_path = Path('dist/Triglyceride_Analysis_System.exe')
    
    if not exe_path.exists():
        print("❌ No se encontró el ejecutable en dist/")
        return False
    
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"✅ Ejecutable creado: {exe_path}")
    print(f"📏 Tamaño: {size_mb:.2f} MB")
    

    shutil.copy(exe_path, 'Triglyceride_Analysis_System.exe')
    print(f"📦 Copiado a: {Path().absolute()}/Triglyceride_Analysis_System.exe")
    
    return True

def create_quick_start_guide():
    """Crea una guía rápida de uso"""
    print("\n📝 Creando guía de uso...")
    
    guide_content = """# 🚀 Guía Rápida - Triglyceride Analysis System

## 📥 Instalación Rápida
1. Descarga `Triglyceride_Analysis_System.exe`
2. Ejecuta directamente (no requiere instalación)

## 🖥️ Primer Uso
1. **Ejecuta** el programa
2. **Ingresa** nombre del experimento
3. **Carga imágenes** por día
4. **Espera** procesamiento automático
5. **Revisa resultados** en carpeta `Results_*`

## 📊 Resultados Generados
- `Graph_Evolution.png` - Evolución temporal
- `Graph_Distribution.png` - Distribución
- `Graph_Summary.png` - Resumen
- `Detailed_Data.csv` - Datos detallados
- `Summary_By_Day.csv` - Estadísticas

## ⚠️ Notas Importantes
- El .exe puede ser detectado por antivirus (es seguro)
- Requiere Windows 10/11 64-bit
- Primera ejecución puede ser lenta

## 🆘 Soporte
Problemas comunes:
1. **Error al abrir**: Ejecuta como administrador
2. **Falta DLL**: Instala Microsoft Visual C++ Redistributable
3. **Imágenes no cargan**: Verifica formato (.png, .jpg, .tif)

📧 Contacto: IPICYT - 25° Aniversario
"""
    
    with open('QUICK_START_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ Guía creada: QUICK_START_GUIDE.txt")

def main():
    """Función principal"""
    print_banner()
    

    clean_previous_builds()
    

    if not check_dependencies():
        print("\n❌ Instala las dependencias faltantes y vuelve a intentar")
        sys.exit(1)
    

    if not build_windows_executable():
        print("\n❌ Falló la construcción del ejecutable")
        sys.exit(1)
    
 
    if not verify_executable():
        print("\n⚠️ Ejecutable creado pero con advertencias")
    

    create_quick_start_guide()
    

    print("\n" + "="*70)
    print("🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
    print("="*70)
    print("\n📋 RESUMEN:")
    print(f"1. Ejecutable principal: Triglyceride_Analysis_System.exe")
    print(f"2. Tamaño: ~{(Path('dist/Triglyceride_Analysis_System.exe').stat().st_size / (1024*1024)):.1f} MB")
    print(f"3. Guía de uso: QUICK_START_GUIDE.txt")
    print(f"4. Para distribuir: Comprime el .exe y la guía")
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Algunos antivirus pueden marcar el .exe como falso positivo")
    print("   - Para distribuirlo, considera firmar el ejecutable digitalmente")
    print("   - Primera ejecución puede ser lenta (extracción de archivos)")
    
    print("\n" + "="*70)
    print("🧪 IPICYT - 25° Aniversario - Sistema de Análisis de Triglicéridos")
    print("="*70)

if __name__ == "__main__":
    main()
