echo 'Checking editorconfig lint...'
ec -e '.venv'

if [ $? -eq 0 ]; then
  echo 'Success'
fi

echo ''
echo 'Checking flake8 lint...'
flake8 --exclude=venv,env,.venv,migrations

if [ $? -eq 0 ]; then
  echo 'Success'
fi


echo ''
echo 'Checking migrations'
python manage.py makemigrations --check --dry-run > /dev/null

if [ $? -eq 0 ]; then
  echo 'Success'
else
  echo 'Missing migrations'
fi
