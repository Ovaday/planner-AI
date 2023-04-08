#!/bin/bash

echo "VERCEL_GIT_COMMIT_REF: $VERCEL_GIT_COMMIT_REF"

if [[ "$VERCEL_GIT_COMMIT_REF" == "mig" ]] ; then
  # Proceed with the build
  echo "✅ - Build can proceed"
  exit 1;
elif [[ "$VERCEL_GIT_COMMIT_REF" == "main" ]] ; then
  # Proceed with the build
  echo "✅ - Build can proceed"
  exit 1;
else
  echo "🛑 - Build is intended to AWS and not for Vercel"
  exit 0;
fi
