NO_TAG="ghcr.io/${1}/qsiqc"
NO_TAG="$(echo "${NO_TAG}" | tr -d '[:space:]')"

docker push --all-tags $NO_TAG