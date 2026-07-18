#!/usr/bin/env python3
"""
WHODIS — Full OSINT Phone Number Investigator

A comprehensive CLI tool for phone number OSINT investigation.
Searches across 13+ sources to identify phone number owners.

Usage:
    whodis -n +62812345678
    whodis -n +62812345678 -s truecaller,whatsapp
    whodis -f numbers.txt -o results.json -v
"""

import sys
import argparse
import json
import csv
from pathlib import Path
from tqdm import tqdm

from whodis.utils import Output, Cache, SOURCES_LIST, VERSION, EMOJIS
from whodis.sources import SOURCES_FUNCTIONS


def validate_number(number: str) -> str:
    """Validate and format phone number."""
    # Add + if not present
    if not number.startswith('+'):
        if number.startswith('0'):
            # Indonesian format
            number = '+62' + number[1:]
        else:
            number = '+' + number
    
    # Basic validation
    if not number.startswith('+'):
        raise ValueError("Invalid phone number format")
    
    return number


def parse_sources(sources_str: str) -> list:
    """Parse sources string and return list."""
    if not sources_str:
        return SOURCES_LIST
    
    sources = [s.strip().lower() for s in sources_str.split(',')]
    # Always include validator
    if 'validator' not in sources:
        sources.insert(0, 'validator')
    
    return sources


def investigate_number(number: str, sources: list, timeout: int = 10, 
                      verbose: bool = False, use_cache: bool = True) -> dict:
    """
    Investigate a phone number across multiple sources.
    
    Args:
        number: Phone number to investigate
        sources: List of sources to check
        timeout: Timeout per request
        verbose: Enable verbose output
        use_cache: Use cache if available
        
    Returns:
        Dictionary with results from all sources
    """
    results = {}
    output = Output()
    
    # Try to get from cache first
    if use_cache:
        cached_results = Cache.get_all_for_number(number)
        if cached_results:
            if verbose:
                output.info(f"Using cached results for {number}")
            return cached_results
    
    # Progress bar
    pbar = tqdm(total=len(sources), desc="Scanning", unit="source", 
                colour='red', ncols=80)
    
    for source in sources:
        try:
            if source in SOURCES_FUNCTIONS:
                func = SOURCES_FUNCTIONS[source]
                result = func(number, timeout=timeout)
                results[source] = result
                
                # Cache the result
                if use_cache and result:
                    Cache.set(number, source, result)
                
                # Print progress
                status = f"{EMOJIS['CHECK']} Found" if result.get('found') else f"{EMOJIS['CROSS']} Not found"
                pbar.update(1)
                
                if verbose:
                    pbar.write(f"[{source:<15}] {status}")
            else:
                pbar.update(1)
                if verbose:
                    pbar.write(f"[{source:<15}] {EMOJIS['WARNING']} Skipped (unknown)")
        except Exception as e:
            results[source] = {
                'found': False,
                'data': {},
                'error': str(e)
            }
            pbar.update(1)
            if verbose:
                pbar.write(f"[{source:<15}] {EMOJIS['CROSS']} Error: {str(e)}")
    
    pbar.close()
    return results


def export_results(results: dict, number: str, output_file: str) -> None:
    """Export results to file."""
    output_path = Path(output_file)
    
    try:
        if output_path.suffix == '.json':
            # Export as JSON
            export_data = {
                'number': number,
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'results': {}
            }
            
            for source, data in results.items():
                if data and data.get('data'):
                    export_data['results'][source] = data['data']
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        elif output_path.suffix == '.csv':
            # Export as CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Number', 'Source', 'Found', 'Data'])
                
                for source, data in results.items():
                    if data:
                        writer.writerow([
                            number,
                            source,
                            data.get('found', False),
                            json.dumps(data.get('data', {}))
                        ])
        
        elif output_path.suffix == '.txt':
            # Export as TXT
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"WHODIS Investigation Report\n")
                f.write(f"Number: {number}\n")
                f.write(f"Timestamp: {__import__('datetime').datetime.now().isoformat()}\n")
                f.write("=" * 60 + "\n\n")
                
                for source, data in results.items():
                    f.write(f"Source: {source}\n")
                    f.write(f"Found: {data.get('found', False)}\n")
                    if data.get('data'):
                        f.write(f"Data:\n")
                        for key, value in data['data'].items():
                            f.write(f"  {key}: {value}\n")
                    f.write("\n")
        
        else:
            raise ValueError(f"Unsupported file format: {output_path.suffix}")
        
        Output.success(f"Results exported to {output_file}")
    
    except Exception as e:
        Output.error(f"Failed to export results: {str(e)}")


def process_number_file(file_path: str, sources: list, timeout: int, 
                       verbose: bool, output_file: str = None) -> None:
    """Process multiple numbers from a file."""
    output = Output()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        output.info(f"Processing {len(numbers)} numbers from {file_path}")
        
        all_results = {}
        
        for number in tqdm(numbers, desc="Processing numbers", unit="number", colour='red'):
            try:
                validated_number = validate_number(number)
                results = investigate_number(validated_number, sources, timeout, verbose)
                all_results[validated_number] = results
            except ValueError as e:
                output.warning(f"Invalid number {number}: {str(e)}")
            except KeyboardInterrupt:
                output.warning("Interrupted by user")
                sys.exit(1)
        
        # Print summary
        found_count = sum(1 for r in all_results.values() 
                         if any(v.get('found') for v in r.values()))
        output.info(f"\nSummary: Found identities for {found_count}/{len(numbers)} numbers")
        
        # Export if requested
        if output_file:
            export_results(all_results, f"Multiple ({len(numbers)})", output_file)
    
    except FileNotFoundError:
        output.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        output.error(f"Error processing file: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='whodis',
        description='WHODIS — Full OSINT Phone Number Investigator',
        epilog='''
Examples:
  whodis -n +62812345678                    # Investigate single number
  whodis -n +62812345678 -s truecaller      # Use specific sources
  whodis -f numbers.txt -o results.json     # Batch process with export
  whodis -n +62812345678 -v -d              # Verbose + deep scan
  whodis -n +62812345678 --no-cache         # Skip cache
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-n', '--number',
                       help='Phone number to investigate (international format: +62...)')
    
    parser.add_argument('-s', '--sources',
                       help='Comma-separated list of sources to use. ' +
                            f'Available: {", ".join(SOURCES_LIST)}')
    
    parser.add_argument('-f', '--file',
                       help='Read phone numbers from file (one per line)')
    
    parser.add_argument('-o', '--output',
                       help='Save results to file (.json, .csv, or .txt)')
    
    parser.add_argument('-j', '--json',
                       action='store_true',
                       help='Output in JSON format')
    
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Enable verbose/debug output')
    
    parser.add_argument('-d', '--deep',
                       action='store_true',
                       help='Enable deep scan (forum & dark web searches)')
    
    parser.add_argument('-t', '--timeout',
                       type=int,
                       default=10,
                       help='Timeout per request in seconds (default: 10)')
    
    parser.add_argument('--no-cache',
                       action='store_true',
                       help='Skip cache and force new requests')
    
    parser.add_argument('--version',
                       action='version',
                       version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()
    
    output = Output()
    output.header()
    
    # Validate arguments
    if not args.number and not args.file:
        parser.print_help()
        output.error("Either --number or --file is required")
        sys.exit(1)
    
    # Parse sources
    sources = parse_sources(args.sources) if args.sources else SOURCES_LIST
    
    # Add forum source if deep scan enabled
    if args.deep and 'forum' not in sources:
        sources.append('forum')
    
    if args.verbose:
        output.info(f"Using sources: {', '.join(sources)}")
        output.info(f"Timeout: {args.timeout}s")
        output.info(f"Cache: {'Disabled' if args.no_cache else 'Enabled'}")
    
    try:
        if args.file:
            # Process multiple numbers
            process_number_file(args.file, sources, args.timeout, 
                              args.verbose, args.output)
        else:
            # Process single number
            number = validate_number(args.number)
            
            if args.verbose:
                output.info(f"Investigating: {number}")
            
            results = investigate_number(number, sources, args.timeout, 
                                        args.verbose, not args.no_cache)
            
            if args.json:
                # Print JSON output
                export_data = {
                    'number': number,
                    'results': {}
                }
                for source, data in results.items():
                    if data and data.get('data'):
                        export_data['results'][source] = data['data']
                
                print(json.dumps(export_data, indent=2, ensure_ascii=False))
            else:
                # Print formatted results
                output.print_results(results, number)
            
            # Export if requested
            if args.output:
                export_results(results, number, args.output)
    
    except ValueError as e:
        output.error(f"Invalid input: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        output.warning("\nInterrupted by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        output.error(f"Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
