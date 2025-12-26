# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import os
import shutil
import glob
from datetime import datetime, timedelta
from typing import Dict
import json

from smart_project_manager.utils import generate_id


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
    def import_data(data_file: str, import_path: str, strategy: str = "merge") -> Dict:
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            import_data.pop('_export_info', None)

            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
            else:
                current_data = {
                    'labels': {},
                    'projects': {},
                    'tasks': {},
                    'subtasks': {}
                }

            if strategy == "replace":
                result_data = import_data
                imported_items = ImportExportService._count_items(import_data)
            else:
                result_data = ImportExportService._merge_data(current_data, import_data)
                imported_items = ImportExportService._count_items(import_data)

            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=4, ensure_ascii=False)

            return {
                'success': True,
                'imported_items': imported_items
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @staticmethod
    def _merge_data(current_data: Dict, import_data: Dict) -> Dict:
        merged_data = current_data.copy()

        if 'labels' in import_data:
            if 'labels' not in merged_data:
                merged_data['labels'] = {}

            for label_id, label_data in import_data['labels'].items():
                new_id = generate_id()
                merged_data['labels'][new_id] = label_data
                merged_data['labels'][new_id]['id'] = new_id

        if 'projects' in import_data:
            if 'projects' not in merged_data:
                merged_data['projects'] = {}

            for project_id, project_data in import_data['projects'].items():
                new_id = generate_id()
                merged_data['projects'][new_id] = project_data
                merged_data['projects'][new_id]['id'] = new_id
                merged_data['projects'][new_id]['tasks'] = []

        if 'tasks' in import_data:
            if 'tasks' not in merged_data:
                merged_data['tasks'] = {}

            for task_id, task_data in import_data['tasks'].items():
                new_id = generate_id()
                merged_data['tasks'][new_id] = task_data
                merged_data['tasks'][new_id]['id'] = new_id

        if 'subtasks' in import_data:
            if 'subtasks' not in merged_data:
                merged_data['subtasks'] = {}

            for subtask_id, subtask_data in import_data['subtasks'].items():
                new_id = generate_id()
                merged_data['subtasks'][new_id] = subtask_data
                merged_data['subtasks'][new_id]['id'] = new_id

        return merged_data

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
                    filename = os.path.basename(backup_file)
                    try:
                        date_str = filename.replace('backup_', '').replace('.json', '')
                        backup_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')

                        if backup_date < cutoff_date:
                            os.remove(backup_file)
                            deleted += 1
                        else:
                            kept += 1
                    except ValueError:
                        kept += 1

            except Exception:
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
            return {'total': 0, 'backups': []}

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
                    filename = os.path.basename(backup_file)
                    try:
                        date_str = filename.replace('backup_', '').replace('.json', '')
                        backup_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                        date_str = backup_date.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        date_str = "Unknown date"

                backups.append({
                    'path': backup_file,
                    'filename': os.path.basename(backup_file),
                    'date': date_str,
                    'size_mb': size / (1024 * 1024)
                })

            except Exception:
                continue

        backups.sort(key=lambda x: x['filename'], reverse=True)
        recent_backups = backups[:10]

        return {
            'total': len(backup_files),
            'total_size_mb': total_size / (1024 * 1024),
            'backups': recent_backups
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
            except Exception:
                continue

        return {
            'deleted': deleted_count,
            'total_size_mb': total_size / (1024 * 1024),
            'total_files': len(backup_files)
        }
