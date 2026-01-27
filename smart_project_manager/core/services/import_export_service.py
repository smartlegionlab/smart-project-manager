# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import shutil
import glob
import json
import tempfile
from datetime import datetime, timedelta
from typing import Dict


class ImportExportService:

    @staticmethod
    def export_data(data_file: str, export_path: str) -> Dict:
        try:
            if not os.path.exists(data_file):
                return {
                    'success': False,
                    'error': f'Source file {data_file} does not exist'
                }

            shutil.copy2(data_file, export_path)

            with open(export_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data['_export_info'] = {
                'export_date': datetime.now().isoformat(),
                'export_app': 'Smart Project Manager',
                'version': '1.0'
            }

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return {
                'success': True,
                'export_path': export_path,
                'export_size': os.path.getsize(export_path)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def import_data(data_file: str, import_path: str) -> Dict:
        try:
            backup_path = ImportExportService._create_temp_backup(data_file)

            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            import_data.pop('_export_info', None)
            import_data.pop('_backup_info', None)

            if not ImportExportService._validate_import_data(import_data):
                if backup_path and os.path.exists(backup_path):
                    shutil.copy2(backup_path, data_file)
                return {
                    'success': False,
                    'error': 'Invalid import data format'
                }

            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(import_data, f, indent=4, ensure_ascii=False)

            if backup_path and os.path.exists(backup_path):
                os.remove(backup_path)

            imported_items = ImportExportService._count_items(import_data)

            return {
                'success': True,
                'imported_items': imported_items
            }

        except Exception as e:
            backup_path = os.path.join(tempfile.gettempdir(), 'smartpm_import_backup.json')
            if os.path.exists(backup_path):
                try:
                    shutil.copy2(backup_path, data_file)
                    os.remove(backup_path)
                except:
                    pass

            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def _create_temp_backup(data_file: str):
        if not os.path.exists(data_file):
            return None

        temp_dir = tempfile.gettempdir()
        backup_path = os.path.join(temp_dir, 'smartpm_import_backup.json')

        try:
            shutil.copy2(data_file, backup_path)
            return backup_path
        except:
            return None

    @staticmethod
    def _validate_import_data(data: Dict) -> bool:
        if not isinstance(data, dict):
            return False

        if not isinstance(data, dict):
            return False

        required_sections = {'labels', 'projects', 'tasks', 'subtasks'}
        for section in required_sections:
            if section not in data:
                return False
            if not isinstance(data[section], dict):
                return False

        return True

    @staticmethod
    def _count_items(data: Dict) -> Dict:
        return {
            'labels': len(data.get('labels', {})),
            'projects': len(data.get('projects', {})),
            'tasks': len(data.get('tasks', {})),
            'subtasks': len(data.get('subtasks', {}))
        }

    @staticmethod
    def create_backup(data_file: str) -> str:
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Cannot create backup: {data_file} does not exist")

        backup_dir = os.path.join(os.path.dirname(data_file), 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'backup_{timestamp}.json')

        shutil.copy2(data_file, backup_path)

        with open(backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data['_backup_info'] = {
            'backup_date': datetime.now().isoformat(),
            'original_file': data_file
        }

        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        ImportExportService.cleanup_old_backups(backup_dir)

        return backup_path

    @staticmethod
    def cleanup_old_backups(backup_dir: str, days_to_keep: int = 30) -> Dict:
        if not os.path.exists(backup_dir):
            return {'deleted': 0, 'kept': 0}

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted = 0
        kept = 0

        backup_files = glob.glob(os.path.join(backup_dir, 'backup_*.json'))

        for backup_file in backup_files:
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                backup_date_str = data.get('_backup_info', {}).get('backup_date')
                if backup_date_str:
                    backup_date = datetime.fromisoformat(backup_date_str)

                    if backup_date < cutoff_date:
                        os.remove(backup_file)
                        deleted += 1
                    else:
                        kept += 1
                else:
                    kept += 1

            except Exception as e:
                print(e)
                kept += 1
                continue

        return {
            'deleted': deleted,
            'kept': kept,
            'cutoff_date': cutoff_date.strftime('%Y-%m-%d')
        }

    @staticmethod
    def get_backup_info(backup_dir: str) -> Dict:
        if not os.path.exists(backup_dir):
            return {'total': 0, 'total_size_mb': 0, 'backups': []}

        backup_files = glob.glob(os.path.join(backup_dir, 'backup_*.json'))
        backups = []
        total_size = 0

        for backup_file in backup_files:
            try:
                size = os.path.getsize(backup_file)
                total_size += size

                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                backup_date_str = data.get('_backup_info', {}).get('backup_date')
                if backup_date_str:
                    backup_date = datetime.fromisoformat(backup_date_str)
                    date_str = backup_date.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    date_str = "Unknown date"

                backups.append({
                    'path': backup_file,
                    'filename': os.path.basename(backup_file),
                    'date': date_str,
                    'size_mb': size / (1024 * 1024)
                })

            except Exception as e:
                print(e)
                continue

        backups.sort(key=lambda x: x['filename'], reverse=True)

        return {
            'total': len(backup_files),
            'total_size_mb': total_size / (1024 * 1024),
            'backups': backups[:10]
        }

    @staticmethod
    def clear_all_backups(backup_dir: str) -> Dict:
        if not os.path.exists(backup_dir):
            return {'deleted': 0, 'total_size_mb': 0}

        backup_files = glob.glob(os.path.join(backup_dir, 'backup_*.json'))

        if not backup_files:
            return {'deleted': 0, 'total_size_mb': 0}

        total_size = 0
        for backup_file in backup_files:
            total_size += os.path.getsize(backup_file)

        deleted_count = 0
        for backup_file in backup_files:
            try:
                os.remove(backup_file)
                deleted_count += 1
            except Exception as e:
                print(e)
                continue

        return {
            'deleted': deleted_count,
            'total_size_mb': total_size / (1024 * 1024),
            'total_files': len(backup_files)
        }
